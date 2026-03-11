import React from 'react';
import { FaTimes, FaCode, FaFileAlt, FaCheckCircle } from 'react-icons/fa';

const AboutModal = ({ onClose }) => {
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content about-modal" onClick={(e) => e.stopPropagation()}>
                <button onClick={onClose} className="close-modal"><FaTimes /></button>

                <div className="about-header">
                    <img src="/assets/shree-ram.png" alt="Shree Ram" className="about-small-logo" />
                    <p className="logo-subtitle">@ Bhadradri Technologies.Inc</p>
                    <h2>🍽️ About This Project</h2>
                    <p className="about-subtitle">South Indian Food Ordering App</p>
                </div>

                <div className="about-content">
                    <div className="stats-grid">
                        <div className="stat-card">
                            <div className="stat-icon">✨</div>
                            <div className="stat-value">12+</div>
                            <div className="stat-label">Major Features</div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-icon"><FaCode /></div>
                            <div className="stat-value">9</div>
                            <div className="stat-label">React Components</div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-icon">📝</div>
                            <div className="stat-value">~2000+</div>
                            <div className="stat-label">Lines of Code</div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-icon"><FaFileAlt /></div>
                            <div className="stat-value">8</div>
                            <div className="stat-label">Documentation Files</div>
                        </div>
                    </div>

                    <div className="status-badge">
                        <FaCheckCircle /> Production-Ready
                    </div>

                    <div className="tech-stack">
                        <h3>Built With</h3>
                        <div className="tech-tags">
                            <span className="tech-tag">React 18</span>
                            <span className="tech-tag">Vite</span>
                            <span className="tech-tag">JavaScript</span>
                            <span className="tech-tag">CSS3</span>
                        </div>
                    </div>

                    <div className="features-list">
                        <h3>Key Features</h3>
                        <ul>
                            <li>✅ Menu Management (CRUD)</li>
                            <li>✅ Shopping Cart System</li>
                            <li>✅ UPI Payment Integration</li>
                            <li>✅ WhatsApp Ordering</li>
                            <li>✅ Smart AI Chatbot</li>
                            <li>✅ Multi-Currency Support</li>
                            <li>✅ Dark Mode Theme</li>
                            <li>✅ Responsive Design</li>
                        </ul>
                    </div>
                </div>

                <div className="about-footer">
                    <div className="copyright">
                        <p>Bhadradri Technologies.Inc</p>
                        <p className="rights">Copyright © 2025</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AboutModal;
