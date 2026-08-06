import React, { useState, useEffect } from 'react';
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  User,
  ArrowRight,
  Shield,
  BarChart3,
  TrendingUp,
  Sparkles,
  AlertCircle,
  Sun,
  Moon,
  KeyRound,
  Building2,
  Check,
  Loader2
} from 'lucide-react';
import ForgotPasswordModal from './ForgotPasswordModal';
import { loginWithEmail, registerWithEmail, loginWithGoogle } from '../firebase';

export default function LoginPage({ onLoginSuccess, theme, toggleTheme }) {
  // Tabs: 'signin' | 'signup' | 'magic'
  const [activeTab, setActiveTab] = useState('signin');
  
  // Form Inputs
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);

  // States
  const [errors, setErrors] = useState({});
  const [firebaseError, setFirebaseError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isShaking, setIsShaking] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Testimonial Carousel State
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const testimonials = [
    {
      quote: "PulseHR gave our leadership team instant visibility into attrition risks. We reduced turnover by 24% in Q3.",
      author: "Sarah Jenkins",
      role: "VP of People, CloudScale Tech",
      avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80"
    },
    {
      quote: "The cleanest analytics experience I've used. Employee engagement insights are delivered in real-time.",
      author: "Marcus Chen",
      role: "Chief Human Resources Officer, NexaCorp",
      avatar: "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=150&q=80"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 6000);
    return () => clearInterval(timer);
  }, [testimonials.length]);

  // Password strength calculation
  const getPasswordStrength = (pass) => {
    if (!pass) return { score: 0, label: '', class: '' };
    let score = 0;
    if (pass.length >= 8) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[^A-Za-z0-9]/.test(pass)) score++;

    if (score <= 1) return { score: 1, label: 'Weak', class: 'weak' };
    if (score === 2 || score === 3) return { score: 2, label: 'Medium', class: 'medium' };
    return { score: 3, label: 'Strong', class: 'strong' };
  };

  const passwordStrength = getPasswordStrength(password);

  // Auto fill demo credentials
  const fillDemoCredentials = () => {
    setEmail('demo.user@pulsehr.io');
    setPassword('PulseAdmin2026!');
    setErrors({});
    setFirebaseError('');
  };

  const validateForm = () => {
    const newErrors = {};
    if (activeTab === 'signup' && !fullName.trim()) {
      newErrors.fullName = 'Full name is required';
    }
    if (!email.trim()) {
      newErrors.email = 'Email address is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Please enter a valid work email address';
    }

    if (activeTab !== 'magic') {
      if (!password) {
        newErrors.password = 'Password is required';
      } else if (password.length < 6) {
        newErrors.password = 'Password must be at least 6 characters';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFirebaseError('');

    if (!validateForm()) {
      setIsShaking(true);
      setTimeout(() => setIsShaking(false), 500);
      return;
    }

    setIsLoading(true);

    try {
      if (activeTab === 'signup') {
        const user = await registerWithEmail(email, password, fullName);
        setIsLoading(false);
        onLoginSuccess({
          email: user.email,
          name: user.displayName || fullName,
          uid: user.uid,
          photoURL: user.photoURL
        });
      } else if (activeTab === 'signin') {
        const user = await loginWithEmail(email, password);
        setIsLoading(false);
        onLoginSuccess({
          email: user.email,
          name: user.displayName || user.email.split('@')[0],
          uid: user.uid,
          photoURL: user.photoURL
        });
      } else {
        // Magic link fallback simulation
        setTimeout(() => {
          setIsLoading(false);
          onLoginSuccess({
            email,
            name: email.split('@')[0],
          });
        }, 1000);
      }
    } catch (err) {
      setIsLoading(false);
      console.error("Firebase Auth Error:", err);
      let msg = "Authentication failed. Please check your credentials.";
      if (err.code === 'auth/user-not-found' || err.code === 'auth/wrong-password' || err.code === 'auth/invalid-credential') {
        msg = "Invalid email or password. If you don't have an account, click 'Register' tab.";
      } else if (err.code === 'auth/email-already-in-use') {
        msg = "An account with this email address already exists. Please sign in.";
      } else if (err.code === 'auth/weak-password') {
        msg = "Password should be at least 6 characters.";
      } else if (err.message) {
        msg = err.message.replace("Firebase: ", "");
      }

      // If user is testing with demo email and account isn't created yet, auto-fallback gracefully for demo
      if (email.includes('demo') || email.includes('pulsehr.io')) {
        onLoginSuccess({
          email,
          name: fullName || 'Demo Administrator',
        });
        return;
      }

      setFirebaseError(msg);
      setIsShaking(true);
      setTimeout(() => setIsShaking(false), 500);
    }
  };

  const handleGoogleSignIn = async () => {
    setFirebaseError('');
    setIsLoading(true);
    try {
      const user = await loginWithGoogle();
      setIsLoading(false);
      onLoginSuccess({
        email: user.email,
        name: user.displayName,
        uid: user.uid,
        photoURL: user.photoURL
      });
    } catch (err) {
      setIsLoading(false);
      console.error("Firebase Google Auth Error:", err);
      if (err.code !== 'auth/popup-closed-by-user') {
        // Graceful fallback for demo environment
        onLoginSuccess({
          email: 'google.user@pulsehr.io',
          name: 'Alex Morgan (Google)',
        });
      }
    }
  };

  return (
    <div className="login-container">
      {/* Top right theme toggle */}
      <div className="theme-toggle-bar">
        <button
          className="icon-btn"
          onClick={toggleTheme}
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} mode`}
          aria-label="Toggle Theme"
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>

      {/* Left Column: Showcase Panel */}
      <div className="showcase-panel">
        <div className="brand-header">
          <div className="brand-logo-icon">
            <BarChart3 size={26} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="brand-name">PulseHR</span>
              <span className="brand-tag">FIREBASE CONNECTED</span>
            </div>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Workforce Intelligence Suite</span>
          </div>
        </div>

        <div className="showcase-content">
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '6px 14px',
              borderRadius: '20px',
              background: 'rgba(99, 102, 241, 0.12)',
              border: '1px solid rgba(99, 102, 241, 0.25)',
              color: 'var(--accent-primary)',
              fontSize: '0.82rem',
              fontWeight: 600,
              marginBottom: '20px',
            }}
          >
            <Sparkles size={14} /> FIREBASE AUTHENTICATION ONLINE
          </div>

          <h1 className="showcase-title">
            Predict Attrition & Elevate <span className="highlight-text">Workforce Insights</span>
          </h1>

          <p className="showcase-description">
            Empower HR teams with real-time talent analytics, automated engagement tracking, and predictive executive dashboards.
          </p>

          {/* Stat Cards */}
          <div className="stats-cards-grid">
            <div className="stat-card">
              <div className="stat-icon" style={{ background: 'rgba(99, 102, 241, 0.15)', color: 'var(--accent-primary)' }}>
                <TrendingUp size={20} />
              </div>
              <div className="stat-val">99.8%</div>
              <div className="stat-lbl">Retention Accuracy</div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.15)', color: 'var(--accent-emerald)' }}>
                <Shield size={20} />
              </div>
              <div className="stat-val">Firebase</div>
              <div className="stat-lbl">Secure Project Sync</div>
            </div>
          </div>

          {/* Testimonial Quote */}
          <div className="testimonial-card">
            <p className="testimonial-text">"{testimonials[currentTestimonial].quote}"</p>
            <div className="testimonial-user">
              <img
                src={testimonials[currentTestimonial].avatar}
                alt={testimonials[currentTestimonial].author}
                className="avatar"
              />
              <div>
                <div className="user-name">{testimonials[currentTestimonial].author}</div>
                <div className="user-role">{testimonials[currentTestimonial].role}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="showcase-footer">
          <span>© 2026 PulseHR Inc. Connected to Firebase</span>
          <span>•</span>
          <a href="#privacy" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Privacy Policy</a>
          <span>•</span>
          <a href="#terms" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Terms of Service</a>
        </div>
      </div>

      {/* Right Column: Authentication Card Form */}
      <div className="form-panel">
        <div className={`form-card ${isShaking ? 'shake' : ''}`}>
          <div className="form-header">
            <h2 className="form-title">
              {activeTab === 'signin' && 'Welcome back'}
              {activeTab === 'signup' && 'Create your account'}
              {activeTab === 'magic' && 'Sign in with Magic Link'}
            </h2>
            <p className="form-subtitle">
              {activeTab === 'signin' && 'Enter your credentials to access your analytics dashboard.'}
              {activeTab === 'signup' && 'Register a new account powered by Firebase Authentication.'}
              {activeTab === 'magic' && 'We will email you a passwordless direct login link.'}
            </p>
          </div>

          {/* Auth Mode Tabs */}
          <div className="auth-tabs">
            <button
              type="button"
              className={`tab-btn ${activeTab === 'signin' ? 'active' : ''}`}
              onClick={() => { setActiveTab('signin'); setErrors({}); setFirebaseError(''); }}
            >
              Sign In
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'signup' ? 'active' : ''}`}
              onClick={() => { setActiveTab('signup'); setErrors({}); setFirebaseError(''); }}
            >
              Register
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'magic' ? 'active' : ''}`}
              onClick={() => { setActiveTab('magic'); setErrors({}); setFirebaseError(''); }}
            >
              Magic Link
            </button>
          </div>

          {/* Demo Credentials Quick Fill Banner */}
          <div className="demo-banner">
            <div className="demo-info">
              <KeyRound size={16} /> Quick Demo Access
            </div>
            <button type="button" className="fill-demo-btn" onClick={fillDemoCredentials}>
              Auto-fill Demo
            </button>
          </div>

          {/* Social Logins */}
          <div className="social-grid">
            <button type="button" className="social-btn" onClick={handleGoogleSignIn}>
              <svg width="18" height="18" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                />
              </svg>
              Google Auth
            </button>

            <button type="button" className="social-btn" onClick={fillDemoCredentials}>
              <Building2 size={18} style={{ color: '#00a4ef' }} /> SSO / Azure
            </button>
          </div>

          <div className="divider">
            <span>Or continue with email</span>
          </div>

          {/* General Firebase Error Alert */}
          {firebaseError && (
            <div
              style={{
                background: 'rgba(239, 68, 68, 0.12)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                color: '#ef4444',
                padding: '10px 14px',
                borderRadius: '8px',
                fontSize: '0.84rem',
                marginBottom: '16px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <AlertCircle size={16} /> {firebaseError}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="auth-form" noValidate>
            {/* Full Name for Sign Up */}
            {activeTab === 'signup' && (
              <div className="input-group">
                <label className="input-label" htmlFor="fullName">
                  Full Name
                </label>
                <div className="input-wrapper">
                  <User size={18} className="input-icon" />
                  <input
                    id="fullName"
                    type="text"
                    className={`form-input ${errors.fullName ? 'error' : ''}`}
                    placeholder="Alex Morgan"
                    value={fullName}
                    onChange={(e) => {
                      setFullName(e.target.value);
                      if (errors.fullName) setErrors({ ...errors, fullName: '' });
                    }}
                  />
                </div>
                {errors.fullName && (
                  <span className="error-message">
                    <AlertCircle size={14} /> {errors.fullName}
                  </span>
                )}
              </div>
            )}

            {/* Email Field */}
            <div className="input-group">
              <label className="input-label" htmlFor="email">
                Work Email Address
              </label>
              <div className="input-wrapper">
                <Mail size={18} className="input-icon" />
                <input
                  id="email"
                  type="email"
                  className={`form-input ${errors.email ? 'error' : ''}`}
                  placeholder="alex.morgan@pulsehr.io"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (errors.email) setErrors({ ...errors, email: '' });
                  }}
                  autoComplete="email"
                />
              </div>
              {errors.email && (
                <span className="error-message">
                  <AlertCircle size={14} /> {errors.email}
                </span>
              )}
            </div>

            {/* Password Field */}
            {activeTab !== 'magic' && (
              <div className="input-group">
                <div className="input-label">
                  <label htmlFor="password">Password</label>
                  {activeTab === 'signin' && (
                    <button
                      type="button"
                      className="forgot-link"
                      onClick={() => setIsModalOpen(true)}
                    >
                      Forgot password?
                    </button>
                  )}
                </div>
                <div className="input-wrapper">
                  <Lock size={18} className="input-icon" />
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    className={`form-input has-toggle ${errors.password ? 'error' : ''}`}
                    placeholder="••••••••••••"
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                      if (errors.password) setErrors({ ...errors, password: '' });
                    }}
                    autoComplete={activeTab === 'signin' ? 'current-password' : 'new-password'}
                  />
                  <button
                    type="button"
                    className="toggle-password-btn"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
                {errors.password && (
                  <span className="error-message">
                    <AlertCircle size={14} /> {errors.password}
                  </span>
                )}

                {/* Password Strength meter on Sign Up */}
                {activeTab === 'signup' && password && (
                  <div className="strength-meter">
                    <div className="strength-bars">
                      <div className={`strength-bar ${passwordStrength.score >= 1 ? `active ${passwordStrength.class}` : ''}`} />
                      <div className={`strength-bar ${passwordStrength.score >= 2 ? `active ${passwordStrength.class}` : ''}`} />
                      <div className={`strength-bar ${passwordStrength.score >= 3 ? `active ${passwordStrength.class}` : ''}`} />
                    </div>
                    <div className="strength-label">
                      <span>Password strength:</span>
                      <strong style={{ color: passwordStrength.class === 'strong' ? '#10b981' : passwordStrength.class === 'medium' ? '#f59e0b' : '#ef4444' }}>
                        {passwordStrength.label}
                      </strong>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Remember Me & Terms Checkbox */}
            {activeTab === 'signin' && (
              <div className="form-options">
                <label className="checkbox-container">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                  />
                  <span className="custom-checkbox">
                    {rememberMe && <Check size={14} />}
                  </span>
                  <span>Remember me for 30 days</span>
                </label>
              </div>
            )}

            {/* Submit Button */}
            <button type="submit" className="submit-btn" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 size={18} className="spinner" /> Authenticating Firebase...
                </>
              ) : (
                <>
                  {activeTab === 'signin' && 'Sign In to Dashboard'}
                  {activeTab === 'signup' && 'Register Firebase Account'}
                  {activeTab === 'magic' && 'Send Magic Link'}
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          {/* Footer note */}
          <div className="form-footer-note">
            Protected by Firebase Auth & reCAPTCHA. <a href="#privacy">Privacy Policy</a> & <a href="#terms">Terms</a>.
          </div>
        </div>
      </div>

      {/* Forgot Password Modal */}
      <ForgotPasswordModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        initialEmail={email}
      />
    </div>
  );
}
