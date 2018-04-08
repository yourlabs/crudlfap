module.exports = {
    "env": {
        "browser": true,
        "es6": true,
        "jest": true
    },
    "extends": "eslint:recommended",
    "parserOptions": {
        "sourceType": "module",
        ecmaVersion: 2017,
        ecmaFeatures: {
            experimentalObjectRestSpread: true,
        }
    },
    "rules": {
        "indent": [
            "error",
            2
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "error",
            "single"
        ],
        "semi": [
            "error",
            "never"
        ],
        "no-cond-assign": "off",
    }
};
