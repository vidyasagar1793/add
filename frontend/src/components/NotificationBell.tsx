import { useState, useEffect, useRef, useCallback, type FC } from 'react';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';

interface Notification {
    id: number;
    message: string;
    is_read: boolean;
    created_at: string;
    article_id?: number;
}

const NotificationBell: FC = () => {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);
    const { token } = useAuth();
    const dropdownRef = useRef<HTMLDivElement>(null);

    const fetchNotifications = useCallback(async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/notifications/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setNotifications(response.data);
            setUnreadCount(response.data.filter((n: Notification) => !n.is_read).length);
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    }, [token]);

    // Poll for notifications every 30 seconds
    useEffect(() => {
        if (!token) return;

        // eslint-disable-next-line
        fetchNotifications();
        const interval = setInterval(fetchNotifications, 30000);

        return () => clearInterval(interval);
    }, [token, fetchNotifications]);

    // Handle outside click to close dropdown
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [dropdownRef]);

    const markAsRead = async (id: number) => {
        try {
            await axios.put(`http://localhost:8000/api/v1/notifications/${id}/read`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            // Optimistic update
            setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
            setUnreadCount(prev => Math.max(0, prev - 1));
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    };

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                type="button"
                className="relative rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                onClick={toggleDropdown}
            >
                <span className="sr-only">View notifications</span>
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
                </svg>
                {unreadCount > 0 && (
                    <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white" />
                )}
            </button>

            {isOpen && (
                <div className="absolute right-0 z-10 mt-2 w-80 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none max-h-96 overflow-y-auto">
                    <div className="px-4 py-2 border-b border-gray-100">
                        <h3 className="text-sm font-semibold text-gray-900">Notifications</h3>
                    </div>
                    {notifications.length === 0 ? (
                        <div className="px-4 py-4 text-sm text-gray-500 text-center">No notifications</div>
                    ) : (
                        notifications.map((notification) => (
                            <div key={notification.id} className={`px-4 py-3 border-b border-gray-50 hover:bg-gray-50 ${!notification.is_read ? 'bg-blue-50' : ''}`}>
                                <p className="text-sm text-gray-900">{notification.message}</p>
                                <div className="mt-1 flex justify-between items-center">
                                    <p className="text-xs text-gray-500">{new Date(notification.created_at).toLocaleDateString()}</p>
                                    {!notification.is_read && (
                                        <button
                                            onClick={(e) => { e.stopPropagation(); markAsRead(notification.id); }}
                                            className="text-xs text-indigo-600 hover:text-indigo-900 font-medium"
                                        >
                                            Mark read
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );
};

export default NotificationBell;
