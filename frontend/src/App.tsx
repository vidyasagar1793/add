import { type ReactElement } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import Login from './components/Login';
import Signup from './components/Signup';
import FeedList from './components/FeedList';
import ArticleStream from './components/ArticleStream';
import TopicSelector from './components/TopicSelector';
import NotificationBell from './components/NotificationBell';

const ProtectedRoute = ({ children }: { children: ReactElement }) => {
  const { token, isLoading } = useAuth();
  console.log('ProtectedRoute: isLoading=', isLoading, 'token=', !!token);

  if (isLoading) {
    return <div className="p-10 text-center">Loading authentication...</div>;
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

function App() {
  console.log('App rendering...');
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <div className="p-8 max-w-7xl mx-auto">
                    <div className="mb-8 flex justify-between items-start">
                      <div>
                        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight mb-4">
                          Content Dashboard
                        </h2>
                        <TopicSelector />
                      </div>
                      <div className="ml-4 flex items-center">
                        <NotificationBell />
                        <span className="ml-3 text-sm font-medium text-gray-500">Welcome!</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
                      <div className="lg:col-span-1">
                        <FeedList />
                      </div>
                      <div className="lg:col-span-2">
                        <ArticleStream />
                      </div>
                    </div>
                  </div>
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
