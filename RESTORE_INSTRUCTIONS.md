# How to Restore Menu Features

The Menu.jsx file needs these features added back:

## 1. Missing Imports
Add to line 2:
```javascript
import { FaTrash, FaPlus, FaRupeeSign, FaCartPlus, FaEdit, FaCog, FaMoon, FaSun, FaInfoCircle, FaTimes } from 'react-icons/fa';
import AboutModal from './AboutModal';
import PasswordModal from './PasswordModal';
```

## 2. Missing State Variables
Add after line 15:
```javascript
// Admin modal states
const [isAdminUnlocked, setIsAdminUnlocked] = useState(false);
const [adminPassword, setAdminPassword] = useState('');
const [showPasswordModal, setShowPasswordModal] = useState(false);
const [passwordAction, setPasswordAction] = useState(null);
const [showAdminModal, setShowAdminModal] = useState(false);
const [showAbout, setShowAbout] = useState(false);
```

## 3. Header Updates
- Change logo to: `/assets/login-food.png`
- Change title to: `South Indian Food`
- Add Admin button before dark mode button
- Add About icon button

## 4. Steam Animation
Add inside `.food-icon` div after the image/video:
```jsx
<div className={`item-smoke-container ${item.name.toLowerCase().includes('idly') ? 'gray-smoke' : ''}`} style={{ display: item.name.toLowerCase().includes('faluda') ? 'none' : 'block' }}>
    <div className="smoke s1"></div>
    <div className="smoke s2"></div>
    <div className="smoke s3"></div>
    <div className="smoke s4"></div>
    <div className="smoke s5"></div>
</div>
```

## 5. Update Edit/Delete Buttons
Change from `onDelete(item.id)` to `handleDeleteClick(item.id, item.name)`
Change from `setEditingItem(item)` to `handleEditClick(item)`
