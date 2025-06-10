/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        // '../templates/**/*.html',
        // '../../templates/**/*.html',
        '../../templates/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        '../../**/templates/**/**/*.html',
        '../../home/index-home.js',
    ],
    theme: {
        extend: {
            colors: {
                "primary": "#f9cc41",
                "primary-light": "#ffb057",
                'secondary-light': '#bac5b9',
                'secondary': '#032900',
                'secondary-dark': '#051900',
                "neutral": "#23282F",
                "info": "#90cbd4",
                "success": "#6CB288",
                "warning": "#fdcb10",
                "error": "#fc483f",
                'facebook': '#3b5998',
                'whatsapp': '#25d366',
                'twitter': '#1DA1F2',
                'mail': '#EA4335',
            },
            height: {
                'screen90': '90vh',
                'screen75': '75vh',
                'screen/2': '50vh',
                'screen/3': 'calc(100vh / 3)',
                'screen/4': 'calc(100vh / 4)',
                'screen/5': 'calc(100vh / 5)',
                'screen400': '400px',
                'screen600': '600px',
                'screen800': '800px',
                'screen1000': '1000px'
            },
            dropShadow: {
                'black': '0px 0px 6px black',
            },
            fontFamily: {
                'nunito': ['"Nunito"','sans-serif'],
                'noto': ['"Noto Serif"','serif']
              },
            animation: {
                "fade-in-fwd": "fade-in-fwd 4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both",
            },
            keyframes: {
                "fade-in-fwd": {
                    "0%": {                        
                        opacity: "0"
                    },
                    to: {                        
                        opacity: "1"
                    }
                },
            },
        },
    },
    plugins: [
        // require('@tailwindcss/aspect-ratio'),
        // require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        // require('@tailwindcss/line-clamp'),
    ],
}
