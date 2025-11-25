import React, { useState, useEffect } from 'react';
import { FaTimes, FaSave, FaCog } from 'react-icons/fa';

const SettingsModal = ({ currentVpa, onSave, onClose, currentCurrency, onSaveCurrency }) => {
    const [vpa, setVpa] = useState('');
    const [currencyCode, setCurrencyCode] = useState('INR');

    useEffect(() => {
        setVpa(currentVpa);
        if (currentCurrency) {
            setCurrencyCode(currentCurrency.code);
        }
    }, [currentVpa, currentCurrency]);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave(vpa);

        // Handle currency save
        const newCurrency = currencyCode === 'USD'
            ? { code: 'USD', symbol: '$', rate: 84 }
            : { code: 'INR', symbol: '₹', rate: 1 };
        onSaveCurrency(newCurrency);
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button onClick={onClose} className="close-modal"><FaTimes /></button>
                <h2><FaCog /> Settings</h2>
                <form onSubmit={handleSubmit} className="settings-form">
                    <div className="form-group">
                        <label>Merchant UPI ID (VPA)</label>
                        <input
                            type="text"
                            value={vpa}
                            onChange={(e) => setVpa(e.target.value)}
                            placeholder="e.g. merchant@upi"
                            required
                        />
                        <small className="hint-text">This ID will be used to generate the QR code for payments.</small>
                    </div>

                    <div className="form-group">
                        <label>Currency</label>
                        <div className="currency-options">
                            <label className={`currency-option ${currencyCode === 'INR' ? 'selected' : ''}`}>
                                <input
                                    type="radio"
                                    name="currency"
                                    value="INR"
                                    checked={currencyCode === 'INR'}
                                    onChange={() => setCurrencyCode('INR')}
                                />
                                <span>Rupees (₹)</span>
                            </label>
                            <label className={`currency-option ${currencyCode === 'USD' ? 'selected' : ''}`}>
                                <input
                                    type="radio"
                                    name="currency"
                                    value="USD"
                                    checked={currencyCode === 'USD'}
                                    onChange={() => setCurrencyCode('USD')}
                                />
                                <span>Dollars ($)</span>
                            </label>
                        </div>
                    </div>

                    <button type="submit" className="save-btn">
                        <FaSave /> Save Settings
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SettingsModal;
