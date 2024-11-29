module.exports = {
    parser: "@typescript-eslint/parser",
    extends: [
        "plugin:@typescript-eslint/recommended",
        "plugin:react/recommended",
        "plugin:prettier/recommended"
    ],
    parserOptions: {
        ecmaVersion: 2020,
        sourceType: "module",
        ecmaFeatures: {
            jsx: true
        }
    },
    plugins: [
        "@typescript-eslint",
        "react",
        "prettier"
    ],
    settings: {
        react: {
            version: "detect"
        }
    },
    rules: {
        "prettier/prettier": ["error", {
            "printWidth": 80,
            "singleQuote": true,
            "trailingComma": "es5"
        }]
    }
};
