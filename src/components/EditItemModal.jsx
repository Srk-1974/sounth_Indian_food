import React, { useState, useEffect } from 'react';
import { FaTimes, FaSave } from 'react-icons/fa';
import assetsList from '../assetsList.json';

const EditItemModal = ({ item, onSave, onClose, currency }) => {
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [category, setCategory] = useState('Snacks');
    const [selectedImage, setSelectedImage] = useState('');
    const [isHot, setIsHot] = useState(true);

    const categories = ['Breakfast', 'Lunch', 'Snacks', 'Beverages'];

    // Stock images available for selection
    const stockImages = [
        { value: '', label: 'No Image (Emoji)' },
        ...assetsList
    ];

    useEffect(() => {
        if (item) {
            setName(item.name);
            // Convert price to selected currency for display
            setPrice((item.price / currency.rate).toFixed(2));
            setCategory(item.category || 'Snacks');
            // Set current image or video or empty string
            setSelectedImage(item.video || item.image || '');
            setIsHot(item.isHot !== undefined ? item.isHot : true);
        }
    }, [item, currency]);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Convert price back to base currency (INR) for saving
        const basePrice = Math.round(parseFloat(price) * currency.rate);
        const updatedItem = { ...item, name, price: basePrice, category, isHot };

        // Reset both
        delete updatedItem.image;
        delete updatedItem.video;

        // Update image or video
        if (selectedImage) {
            if (selectedImage.endsWith('.mp4')) {
                updatedItem.video = selectedImage;
            } else {
                updatedItem.image = selectedImage;
            }
        }

        onSave(updatedItem);
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button onClick={onClose} className="close-modal"><FaTimes /></button>
                <h2>Edit Item</h2>
                <form onSubmit={handleSubmit} className="edit-form">
                    <div className="form-group">
                        <label>Item Name</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Price ({currency.symbol})</label>
                        <input
                            type="number"
                            value={price}
                            onChange={(e) => setPrice(e.target.value)}
                            required
                            step="0.01"
                        />
                    </div>
                    <div className="form-group">
                        <label>Category</label>
                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className="category-selector"
                        >
                            {categories.map((cat) => (
                                <option key={cat} value={cat}>
                                    {cat}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group">
                        <label>Image/Video</label>
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
                    </div>
                    <div className="form-group">
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
                    <button type="submit" className="save-btn">
                        <FaSave /> Save Changes
                    </button>
                </form>
            </div >
        </div >
    );
};

export default EditItemModal;
