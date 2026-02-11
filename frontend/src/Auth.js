import React, { useState, useRef } from 'react';
import './Auth.css';
import translations from './translations';

function Auth({ onLogin, language: initialLanguage, theme: initialTheme, onThemeToggle }) {
  const [isLogin, setIsLogin] = useState(true);
  const [language, setLanguage] = useState(initialLanguage || 'en');
  const [theme, setTheme] = useState(initialTheme || 'light');
  const [showEmailAuth, setShowEmailAuth] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [captchaVerified, setCaptchaVerified] = useState(false);
  const canvasRef = useRef(null);
  const [captchaText, setCaptchaText] = useState('');
  const [userCaptchaInput, setUserCaptchaInput] = useState('');

  const t = translations[language];

  // Generate random captcha text
  const generateCaptcha = React.useCallback(() => {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
    let text = '';
    for (let i = 0; i < 6; i++) {
      text += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setCaptchaText(text);
    drawCaptcha(text);
    setUserCaptchaInput('');
    setCaptchaVerified(false);
  }, []);

  // Draw captcha on canvas
  const drawCaptcha = (text) => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Background with gradient
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, '#1a2235');
    gradient.addColorStop(1, '#0a0e1a');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Add noise lines
    for (let i = 0; i < 5; i++) {
      ctx.strokeStyle = `rgba(0, 212, 255, ${Math.random() * 0.3})`;
      ctx.beginPath();
      ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
      ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
      ctx.stroke();
    }
    
    // Draw text with random positions and rotations
    ctx.font = 'bold 30px Arial';
    ctx.textBaseline = 'middle';
    
    for (let i = 0; i < text.length; i++) {
      ctx.save();
      const x = 20 + i * 30;
      const y = 35 + (Math.random() - 0.5) * 10;
      const angle = (Math.random() - 0.5) * 0.4;
      
      ctx.translate(x, y);
      ctx.rotate(angle);
      
      // Random color for each character
      const colors = ['#00d4ff', '#7b2fff', '#00ff88'];
      ctx.fillStyle = colors[Math.floor(Math.random() * colors.length)];
      ctx.fillText(text[i], 0, 0);
      
      ctx.restore();
    }
    
    // Add noise dots
    for (let i = 0; i < 50; i++) {
      ctx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.3})`;
      ctx.fillRect(
        Math.random() * canvas.width,
        Math.random() * canvas.height,
        2,
        2
      );
    }
  };

  // Initialize captcha when switching to register
  React.useEffect(() => {
    if (!isLogin && !showEmailAuth) {
      // Don't generate captcha for social login
    } else if (!isLogin && showEmailAuth) {
      generateCaptcha();
    }
  }, [isLogin, showEmailAuth, generateCaptcha]);

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const verifyCaptcha = () => {
    if (userCaptchaInput.toLowerCase() === captchaText.toLowerCase()) {
      setCaptchaVerified(true);
      return true;
    } else {
      setCaptchaVerified(false);
      setError(t.captchaFailed);
      generateCaptcha();
      return false;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password || (!isLogin && !formData.username)) {
      setError(t.fillAllFields);
      return;
    }

    if (!validateEmail(formData.email)) {
      setError(t.invalidEmail);
      return;
    }

    if (formData.password.length < 6) {
      setError(t.minPassword);
      return;
    }

    if (!isLogin && !verifyCaptcha()) {
      return;
    }

    setLoading(true);

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        onLogin(data.user, data.token);
      } else {
        setError(data.error || 'Authentication failed');
      }
    } catch (error) {
      console.error('Auth error:', error);
      setError('Connection error. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleOAuthLogin = async (provider) => {
    setLoading(true);
    
    // Open OAuth popup
    const width = 500;
    const height = 600;
    const left = window.screen.width / 2 - width / 2;
    const top = window.screen.height / 2 - height / 2;
    
    const popup = window.open(
      `http://localhost:8000/auth/oauth/${provider}/login`,
      `${provider}_login`,
      `width=${width},height=${height},left=${left},top=${top}`
    );

    // Listen for OAuth callback
    const checkPopup = setInterval(() => {
      try {
        if (popup.closed) {
          clearInterval(checkPopup);
          setLoading(false);
        }
      } catch (e) {
        // Cross-origin error expected
      }
    }, 500);

    // Listen for message from popup
    window.addEventListener('message', (event) => {
      if (event.origin !== 'http://localhost:8000') return;
      
      if (event.data.token && event.data.user) {
        localStorage.setItem('token', event.data.token);
        localStorage.setItem('user', JSON.stringify(event.data.user));
        onLogin(event.data.user, event.data.token);
        popup.close();
      } else if (event.data.error) {
        setError(event.data.error);
        setLoading(false);
      }
    }, { once: true });
  };

  