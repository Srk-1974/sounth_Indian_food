import React, { useState } from 'react';
import { FaUser, FaLock } from 'react-icons/fa';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Trim whitespace to avoid copy-paste errors
        // Allow any username, but enforce strict password
        if (username.trim().length > 0 && password.trim() === 'Admin123') {
            onLogin(username.trim());
        } else {
            setError('Invalid password (must be Admin123)');
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-icon-container">
                    <img src="/assets/south-indian-chef.png" alt="South Indian Food" className="login-icon" />
                    <div className="smoke-container">
                        <div className="smoke s1"></div>
                        <div className="smoke s2"></div>
                        <div className="smoke s3"></div>
                        <div className="smoke s4"></div>
                        <div className="smoke s5"></div>
                    </div>
                </div>
                <h2>Welcome to South Indian Food App</h2>
                <p className="login-copyright">copyright@Bhadradri Technologies.Inc</p>
                <p className="subtitle" style={{ animation: 'slideUp 0.8s ease-out', fontWeight: '600', color: 'black' }}>Login to South Indian Food</p>

                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <FaUser className="icon" />
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div className="input-group">
                        <FaLock className="icon" />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    {error && <p className="error-msg">{error}</p>}
                    <button type="submit" className="login-btn">Login</button>
                </form>
            </div>
        </div>
    );
};

export default Login;
