const { ESLint } = require("eslint");

module.exports = new ESLint({
    useEslintrc: false,
    baseConfig: {
        ignorePatterns: ["/venv/**", "**/node_modules/**", "**/venv/**", "**/dist/**", "**/build/**"],
        parserOptions: {
            ecmaVersion: "latest",
            sourceType: "module",
        },
        env: {
            browser: true,
            es2021: true,
            node: true,
        },
        extends: [
            "eslint:recommended",
            "plugin:@typescript-eslint/recommended"
        ],
        parser: "@typescript-eslint/parser",
        plugins: [
            "@typescript-eslint"
        ],
        rules: {
            // Add your custom rules here
        },
    },
});