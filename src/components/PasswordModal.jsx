import React, { useState } from 'react';
import { FaTimes, FaLock } from 'react-icons/fa';

const PasswordModal = ({ onClose, onSubmit, action, itemName }) => {
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(password);
        setPassword('');
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content password-modal" onClick={(e) => e.stopPropagation()}>
                <button onClick={onClose} className="close-modal"><FaTimes /></button>

                <div className="password-modal-header">
                    <FaLock className="lock-icon" />
                    <h2>Admin Authentication Required</h2>
                    <p className="password-modal-subtitle">
                        {action === 'edit' ? `Edit "${itemName}"` : `Delete "${itemName}"`}
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="password-modal-form">
                    <div className="password-input-wrapper">
                        <input
                            type="password"
                            placeholder="Enter admin password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="password-modal-input"
                            autoFocus
                        />
                    </div>

                    <div className="password-modal-actions">
                        <button type="button" onClick={onClose} className="cancel-btn">
                            Cancel
                        </button>
                        <button type="submit" className="submit-password-btn">
                            {action === 'edit' ? 'Edit Item' : 'Delete Item'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default PasswordModal;
