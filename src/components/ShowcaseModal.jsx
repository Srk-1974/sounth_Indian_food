import React from 'react';
import { FaTimes } from 'react-icons/fa';

const ShowcaseModal = ({ videos, onClose }) => {
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content showcase-modal-content" onClick={(e) => e.stopPropagation()}>
                <button onClick={onClose} className="close-modal">
                    <FaTimes />
                </button>
                <h2 className="showcase-title">🎬 Food Showcase</h2>

                {videos.length === 0 ? (
                    <div className="no-videos-message">
                        <p>No showcase videos added yet.</p>
                        <p>Check back later for delicious updates!</p>
                    </div>
                ) : (
                    <div className="showcase-grid">
                        {videos.map((video, index) => (
                            <div key={index} className="showcase-card">
                                <div className="video-wrapper">
                                    <video
                                        controls
                                        className="showcase-video"
                                        onError={(e) => {
                                            e.target.style.display = 'none';
                                            const errorMsg = e.target.nextElementSibling;
                                            if (errorMsg) errorMsg.style.display = 'block';
                                        }}
                                    >
                                        <source src={video.url} type="video/mp4" />
                                        Your browser does not support the video tag.
                                    </video>
                                    <div
                                        style={{
                                            display: 'none',
                                            padding: '20px',
                                            textAlign: 'center',
                                            backgroundColor: '#fff3cd',
                                            borderRadius: '8px',
                                            color: '#856404'
                                        }}
                                    >
                                        ⚠️ Video not available on this device.<br />
                                        <small>Uploaded videos only work on the device they were uploaded from.</small>
                                    </div>
                                </div>
                                <div className="showcase-details">
                                    <h3>{video.title}</h3>
                                    {video.description && <p>{video.description}</p>}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default ShowcaseModal;
