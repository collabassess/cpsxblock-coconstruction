function CoConstructCPSXBlock(runtime, element, data) {
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/index.js":
/*!**********************!*\
  !*** ./src/index.js ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\n\n// import React, { Component } from \"react\";\n// import ReactDOM from \"react-dom\";\n// import Indicator from \"./indicator/Indicator\";\n\nfunction shortModuleID(moduleID) {\n    var blockPattern = /problem\\+block@(\\w+)/g,\n        shortID = \"\";\n\n    var match = blockPattern.exec(moduleID);\n\n    if (match != null) {\n        shortID = match[1];\n    }\n\n    return shortID;\n}\n\n// Module IDs for the co-constructed vertical subset\nvar providerA = data.providerA,\n    providerB = data.providerB,\n    receiverA = data.receiverA,\n    receiverB = data.receiverB;\n\nfunction updateCount(result) {\n    $('.count', element).text(result.count);\n}\n\nvar handlerUrl = runtime.handlerUrl(element, 'increment_count');\n\n$('p', element).click(function (eventObject) {\n    $.ajax({\n        type: \"POST\",\n        url: handlerUrl,\n        data: JSON.stringify({ \"hello\": \"world\" }),\n        success: updateCount\n    });\n});\n\n$('#problem_' + shortModuleID(receiverA) + ' .problem .action button').click(function (e) {\n    var handle = runtime.handlerUrl(element, 'problem_submit'),\n        ans = $('#input' + shortModuleID(receiverB) + '_2_1')[0].value;\n\n    $.ajax({\n        type: \"POST\",\n        url: handle,\n        data: JSON.stringify({ receiver: receiverA, answer: ans })\n    });\n});\n\n$('#problem_' + shortModuleID(receiverB) + ' .problem .action button').click(function (e) {\n    var handle = runtime.handlerUrl(element, 'problem_submit'),\n        ans = $('#input' + shortModuleID(receiverB) + '_2_1')[0].value;\n\n    $.ajax({\n        type: \"POST\",\n        url: handle,\n        data: JSON.stringify({ receiver: receiverB, answer: ans })\n    });\n});\n\n//# sourceURL=webpack:///./src/index.js?");

/***/ })

/******/ });
}