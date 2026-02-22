import { createContext, useState, useEffect, type ReactNode, type FC } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

interface User {
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  isLoading: boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// const API_URL = 'http://localhost:8000/api/v1';

export const AuthProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (token) {
      try {
        const decoded: any = jwtDecode(token);
        // Check if token is expired
        if (decoded.exp * 1000 < Date.now()) {
          logout();
        } else {
          // Ideally fetch user details from backend here using /users/me
          // For now, just setting email from token if available or generic
          setUser({ email: decoded.sub || 'User' });
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
      } catch (error) {
        logout();
      }
    }
    setIsLoading(false);
  }, [token]);

  const login = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
      {isLoading ? <div className="p-5 text-center text-gray-500">Initializing App...</div> : children}
    </AuthContext.Provider>
  );
};
