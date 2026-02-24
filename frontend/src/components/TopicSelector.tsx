import { useState, useEffect, useCallback, type FC } from 'react';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';

interface Topic {
    id: number;
    name: string;
    slug: string;
}

const TopicSelector: FC = () => {
    const [allTopics, setAllTopics] = useState<Topic[]>([]);
    const [selectedTopicIds, setSelectedTopicIds] = useState<number[]>([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState('');
    const { token } = useAuth();

    const fetchData = useCallback(async () => {
        try {
            setLoading(true);
            const [allTopicsRes, userTopicsRes] = await Promise.all([
                axios.get('http://localhost:8000/api/v1/topics/', {
                    headers: { Authorization: `Bearer ${token}` }
                }),
                axios.get('http://localhost:8000/api/v1/topics/me', {
                    headers: { Authorization: `Bearer ${token}` }
                })
            ]);

            setAllTopics(allTopicsRes.data);
            setSelectedTopicIds(userTopicsRes.data.map((t: Topic) => t.id));
        } catch (error) {
            console.error('Error fetching topics:', error);
        } finally {
            setLoading(false);
        }
    }, [token]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const toggleTopic = (id: number) => {
        if (selectedTopicIds.includes(id)) {
            setSelectedTopicIds(selectedTopicIds.filter(tid => tid !== id));
        } else {
            setSelectedTopicIds([...selectedTopicIds, id]);
        }
    };

    const handleSave = async () => {
        try {
            setMessage('');
            await axios.put(
                'http://localhost:8000/api/v1/topics/me',
                { topic_ids: selectedTopicIds },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setMessage('Preferences saved successfully!');
            setTimeout(() => setMessage(''), 3000);
        } catch (error) {
            console.error('Error saving preferences:', error);
            setMessage('Failed to save preferences.');
        }
    };

    if (loading) return <div>Loading topics...</div>;

    return (
        <div className="bg-white shadow sm:rounded-lg mb-8">
            <div className="px-4 py-5 sm:p-6">
                <h3 className="text-base font-semibold leading-6 text-gray-900">Personalize Your Feed</h3>
                <p className="mt-2 text-sm text-gray-500">Select the topics you are interested in.</p>

                <div className="mt-4 flex flex-wrap gap-2">
                    {allTopics.map((topic) => (
                        <button
                            key={topic.id}
                            onClick={() => toggleTopic(topic.id)}
                            className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ring-1 ring-inset cursor-pointer transition-colors ${selectedTopicIds.includes(topic.id)
                                ? 'bg-indigo-600 text-white ring-indigo-600 hover:bg-indigo-700'
                                : 'bg-white text-gray-700 ring-gray-300 hover:bg-gray-50'
                                }`}
                        >
                            {topic.name}
                        </button>
                    ))}
                </div>

                <div className="mt-5">
                    <button
                        type="button"
                        onClick={handleSave}
                        className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        Save Preferences
                    </button>
                    {message && <span className="ml-4 text-sm text-gray-600">{message}</span>}
                </div>
            </div>
        </div>
    );
};

export default TopicSelector;
