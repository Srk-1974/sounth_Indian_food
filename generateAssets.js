import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const assetsDir = path.join(__dirname, 'public', 'assets');
const outputFile = path.join(__dirname, 'src', 'assetsList.json');

// Supported extensions
const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg'];
const videoExtensions = ['.mp4', '.webm'];

try {
    if (!fs.existsSync(assetsDir)) {
        console.error('Assets directory not found:', assetsDir);
        process.exit(1);
    }

    const files = fs.readdirSync(assetsDir);

    const assets = files
        .filter(file => {
            const ext = path.extname(file).toLowerCase();
            return imageExtensions.includes(ext) || videoExtensions.includes(ext);
        })
        .map(file => {
            const ext = path.extname(file);
            const name = path.basename(file, ext);
            // Format label: replace hyphens/underscores with spaces and capitalize
            const label = name
                .replace(/[-_]/g, ' ')
                .replace(/\b\w/g, c => c.toUpperCase());

            return {
                value: `/assets/${file}`,
                label: label
            };
        });

    // Add "No Image" option at the beginning
    // assets.unshift({ value: '', label: 'No Image (Emoji)' }); 
    // We will handle the "No Image" option in the component itself to keep the data clean

    fs.writeFileSync(outputFile, JSON.stringify(assets, null, 2));
    console.log(`Successfully generated asset list with ${assets.length} items.`);

} catch (err) {
    console.error('Error generating asset list:', err);
    process.exit(1);
}
