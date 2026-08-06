import React, { useState, useEffect } from 'react';
import LoginPage from './components/LoginPage';
import SuccessState from './components/SuccessState';
import { subscribeToAuthChanges, logoutUser } from './firebase';
import './index.css';

export default function App() {
  const [theme, setTheme] = useState('dark');
  const [user, setUser] = useState(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Listen to Firebase Auth real-time state changes
  useEffect(() => {
    const unsubscribe = subscribeToAuthChanges((firebaseUser) => {
      if (firebaseUser) {
        setUser({
          email: firebaseUser.email,
          name: firebaseUser.displayName || firebaseUser.email.split('@')[0],
          uid: firebaseUser.uid,
          photoURL: firebaseUser.photoURL
        });
      } else {
        // Keeps user null if signed out
      }
    });
    return () => unsubscribe();
  }, []);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = async () => {
    try {
      await logoutUser();
    } catch (err) {
      console.warn("Logout error:", err);
    }
    setUser(null);
  };

  return (
    <div className="app-root">
      {/* Background ambient lighting */}
      <div className="ambient-bg">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
        <div className="grid-overlay"></div>
      </div>

      {/* Main Content Area */}
      {user ? (
        <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
          <SuccessState user={user} onLogout={handleLogout} />
        </div>
      ) : (
        <LoginPage
          onLoginSuccess={handleLoginSuccess}
          theme={theme}
          toggleTheme={toggleTheme}
        />
      )}
    </div>
  );
}
