import React, { useState, useEffect } from 'react';
import { FaTrash, FaPlus, FaRupeeSign, FaCartPlus, FaEdit, FaCog, FaMoon, FaSun, FaInfoCircle, FaTimes } from 'react-icons/fa';
import EditItemModal from './EditItemModal';
import SettingsModal from './SettingsModal';
import AboutModal from './AboutModal';
import PasswordModal from './PasswordModal';
import ShowcaseModal from './ShowcaseModal';
import assetsList from '../assetsList.json';

const Menu = ({ items, onAdd, onDelete, onEdit, onAddToCart, user, onLogout, merchantVpa, onUpdateVpa, currency, onUpdateCurrency, darkMode, toggleDarkMode, onOpenAdminDashboard }) => {
    const [newItemName, setNewItemName] = useState('');
    const [newItemPrice, setNewItemPrice] = useState('');
    const [newItemCategory, setNewItemCategory] = useState('Snacks');
    const [selectedImage, setSelectedImage] = useState('');
    const [isHot, setIsHot] = useState(true);
    const [editingItem, setEditingItem] = useState(null);
    const [showSettings, setShowSettings] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('All');

    // Admin modal states
    const [isAdminUnlocked, setIsAdminUnlocked] = useState(false);
    const [adminPassword, setAdminPassword] = useState('');
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [passwordAction, setPasswordAction] = useState(null);
    const [showAdminModal, setShowAdminModal] = useState(false);

    const [showAbout, setShowAbout] = useState(false);
    const [showShowcaseModal, setShowShowcaseModal] = useState(false);
    const [showcaseVideos, setShowcaseVideos] = useState(() => {
        const saved = localStorage.getItem('showcaseVideos');
        return saved ? JSON.parse(saved) : [];
    });
    const [adminActiveTab, setAdminActiveTab] = useState('items'); // 'items' or 'showcase'

    // New video state
    const [newVideoTitle, setNewVideoTitle] = useState('');
    const [newVideoUrl, setNewVideoUrl] = useState('');
    const [newVideoDesc, setNewVideoDesc] = useState('');
    const [videoSourceType, setVideoSourceType] = useState('stock'); // 'stock' or 'upload'
    const [uploadedVideoFile, setUploadedVideoFile] = useState(null);

    // Save showcase videos to localStorage whenever they change
    useEffect(() => {
        localStorage.setItem('showcaseVideos', JSON.stringify(showcaseVideos));
    }, [showcaseVideos]);

    const categories = ['All', 'Breakfast', 'Lunch', 'Snacks', 'Beverages'];

    // Filter items based on search query and category
    const filteredItems = items.filter(item => {
        const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    // Stock images available for selection
    const stockImages = [
        { value: '', label: 'No Image (Emoji)' },
        ...assetsList
    ];

    const handleAdd = (e) => {
        e.preventDefault();
        if (newItemName && newItemPrice) {
            const newItem = {
                name: newItemName,
                price: parseInt(newItemPrice),
                category: newItemCategory,
                isHot: isHot
            };
            if (selectedImage) {
                if (selectedImage.endsWith('.mp4')) {
                    newItem.video = selectedImage;
                } else {
                    newItem.image = selectedImage;
                }
            }
            onAdd(newItem);
            setNewItemName('');
            setNewItemPrice('');
            setSelectedImage('');
            setIsHot(true);
        }
    };

    const handleAddVideo = (e) => {
        e.preventDefault();
        let finalVideoUrl = newVideoUrl;

        if (videoSourceType === 'upload' && uploadedVideoFile) {
            finalVideoUrl = URL.createObjectURL(uploadedVideoFile);
        }

        if (newVideoTitle && finalVideoUrl) {
            const newVideo = {
                title: newVideoTitle,
                url: finalVideoUrl,
                description: newVideoDesc
            };
            setShowcaseVideos([...showcaseVideos, newVideo]);
            setNewVideoTitle('');
            setNewVideoUrl('');
            setNewVideoDesc('');
            setUploadedVideoFile(null);
            // Reset file input if possible, or just rely on state
        }
    };

    const handleDeleteVideo = (index) => {
        const updatedVideos = showcaseVideos.filter((_, i) => i !== index);
        setShowcaseVideos(updatedVideos);
    };

    // Helper to get emoji based on name (simple heuristic)
    const getEmoji = (name) => {
        const n = name.toLowerCase();
        if (n.includes('masala') && n.includes('vada')) return '/assets/masala-vada.png';
        if (n.includes('idly')) return '🍚';
        if (n.includes('dosa') || n.includes('dosha')) return '🥞';
        if (n.includes('vada')) return '🍩';
        if (n.includes('poori')) return '🍘';
        if (n.includes('tea')) return '☕';
        if (n.includes('coffee') || n.includes('coeffe')) return '☕';
        return '🍛';
    };

    const handleAdminUnlock = (e) => {
        e.preventDefault();
        if (adminPassword === 'sriram123') {
            setIsAdminUnlocked(true);
            setAdminPassword('');
        } else {
            alert('❌ Incorrect password! Access denied.');
            setAdminPassword('');
        }
    };

    const handleDeleteClick = (itemId, itemName) => {
        setPasswordAction({ type: 'delete', itemId, itemName });
        setShowPasswordModal(true);
    };

    const handleEditClick = (item) => {
        setPasswordAction({ type: 'edit', item });
        setShowPasswordModal(true);
    };

    const handlePasswordSubmit = (password) => {
        if (password === 'sriram123') {
            if (passwordAction.type === 'delete') {
                onDelete(passwordAction.itemId);
            } else if (passwordAction.type === 'edit') {
                setEditingItem(passwordAction.item);
            }
            setShowPasswordModal(false);
            setPasswordAction(null);
        } else {
            alert('❌ Incorrect password! Access denied.');
        }
    };

    return (
        <div className="menu-container">
            <header className="menu-header" style={{ background: '#FF9933', padding: '15px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <img src="/assets/login-food.png" alt="Logo" style={{ width: '70px', height: '70px', borderRadius: '50%', border: '3px solid white', boxShadow: '0 4px 8px rgba(0,0,0,0.2)' }} />
                    <h1 style={{
                        fontFamily: "'Great Vibes', cursive",
                        fontSize: "4rem",
                        color: "#800020",
                        textShadow: "2px 2px 0px #ffffff, 0 4px 15px rgba(0,0,0,0.2)",
                        margin: 0,
                        fontWeight: "700",
                        lineHeight: "1.1",
                        letterSpacing: "1px"
                    }}>South Indian Food <img src="/assets/sunrise-icon.png" alt="sunrise" style={{ width: "50px", height: "50px", verticalAlign: "middle", marginLeft: "10px" }} /></h1>
                </div>
                <div className="user-info">
                    <span>Hello, {user}</span>
                    <button
                        onClick={() => setShowAdminModal(true)}
                        className="admin-btn"
                        title="Admin Panel"
                    >
                        🔐 Admin
                    </button>
                    <button onClick={() => setShowShowcaseModal(true)} className="admin-btn" title="Food Showcase">
                        🎬 Showcase
                    </button>
                    <button onClick={() => setShowAbout(true)} className="settings-btn" title="About">
                        <FaInfoCircle />
                    </button>
                    <button onClick={toggleDarkMode} className="settings-btn" title="Toggle Dark Mode">
                        {darkMode ? <FaSun /> : <FaMoon />}
                    </button>
                    <button onClick={() => setShowSettings(true)} className="settings-btn" title="Settings">
                        <FaCog />
                    </button>
                    <button onClick={onLogout} className="logout-btn">Logout</button>
                </div>
            </header>

            <div className="menu-content">
                <div className="search-section">
                    <input
                        type="text"
                        placeholder="Search items..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                    />
                </div>

                <div className="category-tabs">
                    {categories.map(category => (
                        <button
                            key={category}
                            className={`category-tab ${selectedCategory === category ? 'active' : ''}`}
                            onClick={() => setSelectedCategory(category)}
                        >
                            {category}
                        </button>
                    ))}
                </div>

                <div className="items-grid">
                    {filteredItems.map((item) => (
                        <div key={item.id} className="food-card">
                            <div className="food-icon">
                                {item.video ? (
                                    <video className="food-video" controls>
                                        <source src={item.video} type="video/mp4" />
                                        Your browser does not support the video tag.
                                    </video>
                                ) : item.image ? (
                                    <img src={item.image} alt={item.name} className="food-image" />
                                ) : (
                                    (() => {
                                        const emojiOrPath = getEmoji(item.name);
                                        return emojiOrPath.startsWith('/') ? (
                                            <img src={emojiOrPath} alt={item.name} className="food-image" />
                                        ) : (
                                            emojiOrPath
                                        );
                                    })()
                                )}

                                <div className={`item-smoke-container ${item.name.toLowerCase().includes('idly') ? 'gray-smoke' : ''}`}
                                    style={{
                                        display: (item.isHot !== undefined ? item.isHot : !['faluda', 'badam', 'juice', 'shake', 'ice', 'cool', 'lassi'].some(keyword => item.name.toLowerCase().includes(keyword))) ? 'block' : 'none'
                                    }}>
                                    <div className="smoke s1"></div>
                                    <div className="smoke s2"></div>
                                    <div className="smoke s3"></div>
                                    <div className="smoke s4"></div>
                                    <div className="smoke s5"></div>
                                </div>
                            </div>
                            <div className="food-details">
                                <h3>{item.name}</h3>
                                <p className="price">{currency.symbol} {(item.price / currency.rate).toFixed(2)}</p>
                            </div>
                            <div className="card-actions">
                                <button onClick={() => onAddToCart(item)} className="cart-btn">
                                    <FaCartPlus /> Add to Cart
                                </button>
                            </div>
                            <div className="action-buttons">
                                <button onClick={() => handleEditClick(item)} className="edit-btn" title="Edit Item">
                                    <FaEdit />
                                </button>
                                <button onClick={() => handleDeleteClick(item.id, item.name)} className="delete-btn" title="Delete Item">
                                    <FaTrash />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            {editingItem && (
                <EditItemModal
                    item={editingItem}
                    onSave={(updatedItem) => {
                        onEdit(updatedItem);
                        setEditingItem(null);
                    }}
                    onClose={() => setEditingItem(null)}
                    currency={currency}
                />
            )}
            {showSettings && (
                <SettingsModal
                    currentVpa={merchantVpa}
                    onSave={(newVpa) => {
                        onUpdateVpa(newVpa);
                    }}
                    currentCurrency={currency}
                    onSaveCurrency={(newCurrency) => {
                        onUpdateCurrency(newCurrency);
                        setShowSettings(false);
                    }}
                    onClose={() => setShowSettings(false)}
                />
            )}
            {showAdminModal && (
                <div className="modal-overlay" onClick={() => setShowAdminModal(false)}>
                    <div className="modal-content admin-modal-content" onClick={(e) => e.stopPropagation()}>
                        <button onClick={() => setShowAdminModal(false)} className="close-modal">
                            <FaTimes />
                        </button>

                        <h2 className="admin-modal-title">🔐 Admin Panel</h2>

                        <div className="add-item-section">
                            <h3>🔒 Add New Item (Admin Only)</h3>

                            {!isAdminUnlocked ? (
                                <form onSubmit={handleAdminUnlock} className="admin-unlock-form">
                                    <div className="unlock-message">
                                        <p>🔐 This section is password protected</p>
                                        <p className="unlock-hint">Enter admin password to add new items</p>
                                    </div>
                                    <div className="password-input-group">
                                        <input
                                            type="password"
                                            placeholder="Enter admin password"
                                            value={adminPassword}
                                            onChange={(e) => setAdminPassword(e.target.value)}
                                            className="admin-password-input"
                                        />
                                        <button type="submit" className="unlock-btn">Unlock</button>
                                    </div>
                                </form>
                            ) : (
                                <>
                                    <div className="admin-unlocked-badge">
                                        ✅ Admin Access Granted
                                        <button onClick={() => setIsAdminUnlocked(false)} className="lock-btn">🔒 Lock</button>
                                    </div>

                                    <button
                                        onClick={() => {
                                            setShowAdminModal(false);
                                            onOpenAdminDashboard();
                                        }}
                                        className="view-dashboard-btn"
                                        style={{
                                            width: '100%',
                                            margin: '10px 0',
                                            padding: '10px',
                                            backgroundColor: '#4a90e2',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '5px',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            gap: '8px',
                                            fontSize: '1rem'
                                        }}
                                    >
                                        📊 View Login Activity
                                    </button>

                                    <div className="admin-tabs">
                                        <button
                                            className={`admin-tab ${adminActiveTab === 'items' ? 'active' : ''}`}
                                            onClick={() => setAdminActiveTab('items')}
                                        >
                                            Add Items
                                        </button>
                                        <button
                                            className={`admin-tab ${adminActiveTab === 'showcase' ? 'active' : ''}`}
                                            onClick={() => setAdminActiveTab('showcase')}
                                        >
                                            Manage Showcase
                                        </button>
                                    </div>

                                    {adminActiveTab === 'items' ? (
                                        <form onSubmit={handleAdd} className="add-form">
                                            <input
                                                type="text"
                                                placeholder="Item Name (e.g. Upma)"
                                                value={newItemName}
                                                onChange={(e) => setNewItemName(e.target.value)}
                                            />
                                            <input
                                                type="number"
                                                placeholder="Price (₹)"
                                                value={newItemPrice}
                                                onChange={(e) => setNewItemPrice(e.target.value)}
                                            />
                                            <select
                                                value={newItemCategory}
                                                onChange={(e) => setNewItemCategory(e.target.value)}
                                                className="category-selector"
                                            >
                                                {categories.filter(c => c !== 'All').map(category => (
                                                    <option key={category} value={category}>{category}</option>
                                                ))}
                                            </select>
                                            <select
                                                value={selectedImage}
                                                onChange={(e) => setSelectedImage(e.target.value)}
                                                className="image-selector"
                                            >
                                                {stockImages.map((img) => (
                                                    <option key={img.value} value={img.value}>
                                                        {img.label}
                                                    </option>
                                                ))}
                                            </select>

                                            <div className="hot-toggle-container" style={{ display: 'flex', alignItems: 'center', gap: '10px', margin: '10px 0' }}>
                                                <label style={{ display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
                                                    <input
                                                        type="checkbox"
                                                        checked={isHot}
                                                        onChange={(e) => setIsHot(e.target.checked)}
                                                        style={{ width: 'auto' }}
                                                    />
                                                    {isHot ? '🔥 Hot (Show Steam)' : '❄️ Cold (No Steam)'}
                                                </label>
                                            </div>

                                            <button type="submit" className="add-btn"><FaPlus /> Add Item</button>
                                        </form>
                                    ) : (
                                        <div className="showcase-manager">
                                            <h4>Add New Video</h4>
                                            <form onSubmit={handleAddVideo} className="add-form">
                                                <input
                                                    type="text"
                                                    placeholder="Video Title"
                                                    value={newVideoTitle}
                                                    onChange={(e) => setNewVideoTitle(e.target.value)}
                                                    required
                                                />
                                                <input
                                                    type="text"
                                                    placeholder="Description (Optional)"
                                                    value={newVideoDesc}
                                                    onChange={(e) => setNewVideoDesc(e.target.value)}
                                                />

                                                <div className="video-source-toggle" style={{ margin: '10px 0', display: 'flex', gap: '15px' }}>
                                                    <label style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}>
                                                        <input
                                                            type="radio"
                                                            name="videoSource"
                                                            checked={videoSourceType === 'stock'}
                                                            onChange={() => setVideoSourceType('stock')}
                                                        />
                                                        Select Stock Video
                                                    </label>
                                                    <label style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}>
                                                        <input
                                                            type="radio"
                                                            name="videoSource"
                                                            checked={videoSourceType === 'upload'}
                                                            onChange={() => setVideoSourceType('upload')}
                                                        />
                                                        Upload from Device
                                                    </label>
                                                </div>

                                                {videoSourceType === 'stock' ? (
                                                    <select
                                                        value={newVideoUrl}
                                                        onChange={(e) => setNewVideoUrl(e.target.value)}
                                                        className="image-selector"
                                                        required={videoSourceType === 'stock'}
                                                    >
                                                        <option value="">Select Video...</option>
                                                        {stockImages.filter(img => img.value.endsWith('.mp4')).map((img) => (
                                                            <option key={img.value} value={img.value}>
                                                                {img.label}
                                                            </option>
                                                        ))}
                                                        <option value="/assets/sample-video.mp4">Sample Video (if available)</option>
                                                    </select>
                                                ) : (
                                                    <div className="file-upload-container">
                                                        <input
                                                            type="file"
                                                            accept="video/*"
                                                            onChange={(e) => setUploadedVideoFile(e.target.files[0])}
                                                            required={videoSourceType === 'upload'}
                                                            className="file-input"
                                                            style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '4px', width: '100%' }}
                                                        />
                                                        {uploadedVideoFile && <p style={{ fontSize: '0.8rem', color: 'green', marginTop: '5px' }}>Selected: {uploadedVideoFile.name}</p>}
                                                    </div>
                                                )}

                                                <button type="submit" className="add-btn"><FaPlus /> Add Video</button>
                                            </form>

                                            <h4>Existing Videos</h4>
                                            {showcaseVideos.length === 0 ? (
                                                <p className="no-items">No videos added yet.</p>
                                            ) : (
                                                <ul className="video-list">
                                                    {showcaseVideos.map((video, index) => (
                                                        <li key={index} className="video-item">
                                                            <span>{video.title}</span>
                                                            <button onClick={() => handleDeleteVideo(index)} className="delete-btn-small">
                                                                <FaTrash />
                                                            </button>
                                                        </li>
                                                    ))}
                                                </ul>
                                            )}
                                        </div>
                                    )}
                                </>
                            )}
                        </div>
                    </div>
                </div>
            )}
            {showShowcaseModal && (
                <ShowcaseModal
                    videos={showcaseVideos}
                    onClose={() => setShowShowcaseModal(false)}
                />
            )}
            {showAbout && (
                <AboutModal onClose={() => setShowAbout(false)} />
            )}
            {showPasswordModal && passwordAction && (
                <PasswordModal
                    onClose={() => {
                        setShowPasswordModal(false);
                        setPasswordAction(null);
                    }}
                    onSubmit={handlePasswordSubmit}
                    action={passwordAction.type}
                    itemName={passwordAction.itemName || passwordAction.item?.name}
                />
            )}
        </div>
    );
};

export default Menu;
