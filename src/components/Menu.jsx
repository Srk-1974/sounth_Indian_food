import React, { useState } from 'react';
import { FaTrash, FaPlus, FaRupeeSign, FaCartPlus, FaEdit, FaCog, FaMoon, FaSun } from 'react-icons/fa';
import EditItemModal from './EditItemModal';
import SettingsModal from './SettingsModal';
import assetsList from '../assetsList.json';

const Menu = ({ items, onAdd, onDelete, onEdit, onAddToCart, user, onLogout, merchantVpa, onUpdateVpa, currency, onUpdateCurrency, darkMode, toggleDarkMode }) => {
    const [newItemName, setNewItemName] = useState('');
    const [newItemPrice, setNewItemPrice] = useState('');
    const [newItemCategory, setNewItemCategory] = useState('Snacks');
    const [selectedImage, setSelectedImage] = useState('');
    const [editingItem, setEditingItem] = useState(null);
    const [showSettings, setShowSettings] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('All');

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
                category: newItemCategory
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
        }
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

    return (
        <div className="menu-container">
            <header className="menu-header">
                <div className="logo-container">
                    <img src="/assets/logo.png" alt="South Indian Delights Logo" className="app-logo" />
                    <h1>South Indian Delights</h1>
                </div>
                <div className="user-info">
                    <span>Hello, {user}</span>
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

                <div className="add-item-section">
                    <h3>Add New Item</h3>
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
                        <button type="submit" className="add-btn"><FaPlus /> Add</button>
                    </form>
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
                                <button onClick={() => setEditingItem(item)} className="edit-btn" title="Edit Item">
                                    <FaEdit />
                                </button>
                                <button onClick={() => onDelete(item.id)} className="delete-btn" title="Delete Item">
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
        </div>
    );
};

export default Menu;
