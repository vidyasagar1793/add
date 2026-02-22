import { useState, useEffect, type FC, type FormEvent } from 'react';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';

interface Feed {
    id: number;
    name: string;
    url: string;
    is_active: boolean;
    last_fetched_at: string | null;
}

const FeedList: FC = () => {
    const [feeds, setFeeds] = useState<Feed[]>([]);
    const [name, setName] = useState('');
    const [url, setUrl] = useState('');
    const [message, setMessage] = useState('');
    const { token } = useAuth();

    useEffect(() => {
        fetchFeeds();
    }, []);

    const fetchFeeds = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/feeds/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setFeeds(response.data);
        } catch (error) {
            console.error('Error fetching feeds:', error);
        }
    };

    const handleAddFeed = async (e: FormEvent) => {
        e.preventDefault();
        setMessage('');
        try {
            await axios.post('http://localhost:8000/api/v1/feeds/', { name, url }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setName('');
            setUrl('');
            fetchFeeds();
            setMessage('Feed added successfully!');
        } catch (error) {
            console.error('Error adding feed:', error);
            setMessage('Failed to add feed.');
        }
    };

    const handleRefresh = async (id: number) => {
        try {
            const response = await axios.post(`http://localhost:8000/api/v1/feeds/${id}/refresh`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMessage(`Refreshed! New articles: ${response.data.new_articles}`);
            fetchFeeds();
        } catch (error) {
            console.error("Error refreshing feed", error);
            setMessage("Failed to refresh feed.");
        }
    }

    return (
        <div className="bg-white shadow sm:rounded-lg mb-8">
            <div className="px-4 py-5 sm:p-6">
                <h3 className="text-base font-semibold leading-6 text-gray-900">Manage Feeds</h3>

                <form className="mt-5 sm:flex sm:items-center" onSubmit={handleAddFeed}>
                    <div className="w-full sm:max-w-xs">
                        <label htmlFor="name" className="sr-only">Name</label>
                        <input
                            type="text"
                            name="name"
                            id="name"
                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            placeholder="Source Name (e.g. TechCrunch)"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="w-full sm:max-w-xs sm:ml-4 mt-3 sm:mt-0">
                        <label htmlFor="url" className="sr-only">URL</label>
                        <input
                            type="url"
                            name="url"
                            id="url"
                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            placeholder="RSS URL"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="mt-3 inline-flex w-full items-center justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:ml-3 sm:mt-0 sm:w-auto"
                    >
                        Add Feed
                    </button>
                </form>
                {message && <p className="mt-2 text-sm text-gray-600">{message}</p>}

                <div className="mt-8 flow-root">
                    <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                        <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                            <table className="min-w-full divide-y divide-gray-300">
                                <thead>
                                    <tr>
                                        <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">Name</th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">URL</th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Last Fetched</th>
                                        <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-0">
                                            <span className="sr-only">Actions</span>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                    {feeds.map((feed) => (
                                        <tr key={feed.id}>
                                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0">{feed.name}</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{feed.url}</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{feed.last_fetched_at ? new Date(feed.last_fetched_at).toLocaleString() : 'Never'}</td>
                                            <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                                                <button onClick={() => handleRefresh(feed.id)} className="text-indigo-600 hover:text-indigo-900">Refresh</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FeedList;
