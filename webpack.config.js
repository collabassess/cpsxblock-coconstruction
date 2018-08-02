const path          = require("path");
const WrapperPlugin = require("wrapper-webpack-plugin");

const JS_HANDLE = "CoConstructCPSXBlock";

module.exports = { 
    entry: "./src/index.js",
    output: {
        filename: "constructcpsxblock.js",
        path: path.resolve(__dirname, "constructcpsxblock/constructcpsxblock/static/js/src/")
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            }
        ]
    },
    plugins: [
        new WrapperPlugin({
            test: /\.js$/,
            header: `function ${JS_HANDLE}(runtime, element, data) {\n`,
            footer: '\n}'
        })
    ]
};
