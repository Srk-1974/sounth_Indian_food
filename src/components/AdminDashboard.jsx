import React, { useState, useEffect } from 'react';
import { collection, query, orderBy, limit, getDocs } from 'firebase/firestore';
import { db } from '../config/firebase';
import { FaUsers, FaSignInAlt, FaClock, FaArrowLeft, FaSync } from 'react-icons/fa';
import '../admin-dashboard.css';

const AdminDashboard = ({ onBack }) => {
    const [loginRecords, setLoginRecords] = useState([]);
    const [stats, setStats] = useState({
        totalLogins: 0,
        uniqueUsers: 0,
        todayLogins: 0
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchLoginData();
    }, []);

    const fetchLoginData = async () => {
        setLoading(true);
        setError('');
        try {
            const q = query(
                collection(db, 'loginActivity'),
                orderBy('timestamp', 'desc'),
                limit(50)
            );

            const querySnapshot = await getDocs(q);
            const records = [];
            const uniqueUsers = new Set();
            let todayCount = 0;
            const today = new Date().setHours(0, 0, 0, 0);

            querySnapshot.forEach((doc) => {
                const data = doc.data();
                records.push({ id: doc.id, ...data });
                uniqueUsers.add(data.username);

                const loginDate = data.timestamp?.toDate();
                if (loginDate && loginDate.setHours(0, 0, 0, 0) === today) {
                    todayCount++;
                }
            });

            setLoginRecords(records);
            setStats({
                totalLogins: records.length,
                uniqueUsers: uniqueUsers.size,
                todayLogins: todayCount
            });
            setLoading(false);
        } catch (error) {
            console.error('Error fetching login data:', error);
            setError('Failed to load login data. Please check Firebase configuration.');
            setLoading(false);
        }
    };

    const formatTimestamp = (timestamp) => {
        if (!timestamp) return 'N/A';
        try {
            const date = timestamp.toDate();
            return date.toLocaleString('en-IN', {
                day: 'numeric',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (e) {
            return 'Invalid Date';
        }
    };

    if (loading) {
        return (
            <div className="admin-dashboard">
                <div className="admin-loading">
                    <div className="loading-spinner"></div>
                    <p>Loading dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="admin-dashboard">
            <div className="admin-header">
                <button onClick={onBack} className="back-btn">
                    <FaArrowLeft /> Back to Menu
                </button>
                <h1>🔐 Admin Dashboard</h1>
                <button onClick={fetchLoginData} className="refresh-btn">
                    <FaSync /> Refresh
                </button>
            </div>

            {error && (
                <div className="error-banner">
                    ⚠️ {error}
                </div>
            )}

            <div className="stats-grid">
                <div className="stat-card">
                    <FaSignInAlt className="stat-icon" />
                    <h3>Total Logins</h3>
                    <p className="stat-value">{stats.totalLogins}</p>
                    <span className="stat-label">Last 50 records</span>
                </div>
                <div className="stat-card">
                    <FaUsers className="stat-icon" />
                    <h3>Unique Users</h3>
                    <p className="stat-value">{stats.uniqueUsers}</p>
                    <span className="stat-label">Different usernames</span>
                </div>
                <div className="stat-card">
                    <FaClock className="stat-icon" />
                    <h3>Today's Logins</h3>
                    <p className="stat-value">{stats.todayLogins}</p>
                    <span className="stat-label">{new Date().toLocaleDateString('en-IN')}</span>
                </div>
            </div>

            <div className="login-records">
                <h2>📋 Recent Login Activity</h2>
                {loginRecords.length === 0 ? (
                    <div className="no-data">
                        <p>No login records found. Login tracking will start after users log in.</p>
                    </div>
                ) : (
                    <div className="table-container">
                        <table className="records-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Username</th>
                                    <th>Login Time</th>
                                    <th>Browser</th>
                                    <th>Device</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loginRecords.map((record, index) => (
                                    <tr key={record.id}>
                                        <td>{index + 1}</td>
                                        <td className="username-cell">{record.username}</td>
                                        <td>{formatTimestamp(record.timestamp)}</td>
                                        <td>{record.browser || 'Unknown'}</td>
                                        <td>{record.device || 'Unknown'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminDashboard;
