import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '../config/firebase';

/**
 * Track user login activity in Firebase Firestore
 * @param {string} username - The username of the logged-in user
 */
export const trackLogin = async (username) => {
    try {
        const loginData = {
            username: username,
            timestamp: serverTimestamp(),
            browser: getBrowserInfo(),
            device: getDeviceInfo(),
            userAgent: navigator.userAgent
        };

        await addDoc(collection(db, 'loginActivity'), loginData);
        console.log('✅ Login tracked successfully for:', username);
        return true;
    } catch (error) {
        console.error('❌ Error tracking login:', error);
        // Don't block login if tracking fails
        return false;
    }
};

/**
 * Detect browser from user agent
 */
const getBrowserInfo = () => {
    const ua = navigator.userAgent;
    if (ua.includes('Chrome') && !ua.includes('Edg')) return 'Chrome';
    if (ua.includes('Safari') && !ua.includes('Chrome')) return 'Safari';
    if (ua.includes('Firefox')) return 'Firefox';
    if (ua.includes('Edg')) return 'Edge';
    if (ua.includes('Opera') || ua.includes('OPR')) return 'Opera';
    return 'Other';
};

/**
 * Detect device type from user agent
 */
const getDeviceInfo = () => {
    const ua = navigator.userAgent;
    if (/mobile/i.test(ua)) return 'Mobile';
    if (/tablet|ipad/i.test(ua)) return 'Tablet';
    return 'Desktop';
};
