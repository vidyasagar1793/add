import { createContext, useState, useEffect, useCallback, type ReactNode, type FC } from 'react';
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

interface DecodedToken {
  sub: string;
  exp: number;
}

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Helper to validate token synchronously
const getInitialToken = (): string | null => {
  const token = localStorage.getItem('token');
  if (!token) return null;

  try {
    const decoded = jwtDecode<DecodedToken>(token);
    if (decoded.exp * 1000 < Date.now()) {
      localStorage.removeItem('token');
      return null;
    }
    return token;
  } catch {
    localStorage.removeItem('token');
    return null;
  }
};

export const AuthProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(getInitialToken());
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = useCallback((newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  }, []);

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode<DecodedToken>(token);
        // Double check if token is expired (though getInitialToken handles initial load)
        // If token was just set via login(), it should be valid.
        if (decoded.exp * 1000 < Date.now()) {
          // eslint-disable-next-line
          logout();
        } else {
          setUser({ email: decoded.sub || 'User' });
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
      } catch {
        logout();
      }
    } else {
        setUser(null);
        delete axios.defaults.headers.common['Authorization'];
    }
    setIsLoading(false);
  }, [token, logout]);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
      {isLoading ? <div className="p-5 text-center text-gray-500">Initializing App...</div> : children}
    </AuthContext.Provider>
  );
};
