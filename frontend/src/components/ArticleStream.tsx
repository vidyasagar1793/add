import { useState, useEffect, type FC } from 'react';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';

interface Article {
    id: number;
    title: string;
    summary: string;
    url: string;
    published_at: string;
    topics: Topic[];
    view_count: number;
}

interface Topic {
    id: number;
    name: string;
    slug: string;
}

const ArticleStream: FC = () => {
    const [articles, setArticles] = useState<Article[]>([]);
    const { token } = useAuth();

    useEffect(() => {
        if (token) {
            fetchArticles();
        }
    }, [token]);

    const fetchArticles = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/articles/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setArticles(response.data);
        } catch (error) {
            console.error('Error fetching articles:', error);
        }
    };

    const handleArticleClick = async (articleId: number, url: string) => {
        // Increment view count via API
        try {
            await axios.post(`http://localhost:8000/api/v1/analytics/article/${articleId}/view`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            // Update local state to reflect increment
            setArticles(prev => prev.map(a => a.id === articleId ? { ...a, view_count: a.view_count + 1 } : a));
        } catch (error) {
            console.error("Error updating view count:", error);
        }

        // Open article in new tab
        window.open(url, '_blank');
    };

    return (
        <div className="space-y-6">
            <h3 className="text-xl font-bold text-gray-900">Latest Articles</h3>
            {articles.map((article) => (
                <div key={article.id} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                    <div className="flex justify-between items-start">
                        <h4
                            className="text-lg font-semibold text-gray-900 mb-2 cursor-pointer hover:text-indigo-600"
                            onClick={() => handleArticleClick(article.id, article.url)}
                        >
                            {article.title}
                        </h4>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            👁️ {article.view_count}
                        </span>
                    </div>

                    <p className="text-gray-600 mb-4">{article.summary || "No summary available."}</p>

                    <div className="flex flex-wrap gap-2 mb-3">
                        {article.topics?.map(topic => (
                            <span key={topic.id} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                {topic.name}
                            </span>
                        ))}
                    </div>

                    <div className="flex justify-between items-center text-sm text-gray-500">
                        <span>{article.published_at ? new Date(article.published_at).toLocaleDateString() : 'Unknown Date'}</span>
                        <button
                            onClick={() => handleArticleClick(article.id, article.url)}
                            className="text-indigo-600 hover:text-indigo-800 font-medium"
                        >
                            Read more →
                        </button>
                    </div>
                </div>
            ))}
            {articles.length === 0 && (
                <div className="text-center text-gray-500 py-10">
                    No articles found. Add some feeds to get started!
                </div>
            )}
        </div>
    );
};

export default ArticleStream;
