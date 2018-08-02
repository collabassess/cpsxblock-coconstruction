import React from "react";
import ReactDOM from "react-dom";
import Indicator from "./indicator/Indicator";

function updateCount(result) {
    $('.count', element).text(result.count);
}

var handlerUrl = runtime.handlerUrl(element, 'increment_count');

$('p', element).click(function(eventObject) {
    $.ajax({
        type: "POST",
        url: handlerUrl,
        data: JSON.stringify({"hello": "world"}),
        success: updateCount
    });
});

$(function ($) {
    alert('hello');
    ReactDOM.render(<Indicator />, document.getElementById("component-test"))
});