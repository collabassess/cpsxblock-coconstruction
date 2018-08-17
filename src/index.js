// import React, { Component } from "react";
// import ReactDOM from "react-dom";
// import Indicator from "./indicator/Indicator";

function shortModuleID(moduleID) {
    let blockPattern = /problem\+block@(\w+)/g,
        shortID      = "";
    
    let match = blockPattern.exec(moduleID);

    if (match != null) {
        shortID = match[1];
    }

    return shortID;
}

// Module IDs for the co-constructed vertical subset
const providerA = data.providerA,
      providerB = data.providerB,
      receiverA = data.receiverA,
      receiverB = data.receiverB;

$(`#problem_${shortModuleID(receiverA)} .problem .action button`).click(e => {
    let handle = runtime.handlerUrl(element, 'problem_submit'),
        ans    = $(`#input_${shortModuleID(receiverA)}_2_1`)[0].value;

    $.ajax({
        type: "POST",
        url: handle,
        data: JSON.stringify({receiver: receiverA, answer: ans})
    });
});

$(`#problem_${shortModuleID(receiverB)} .problem .action button`).click(e => {
    let handle = runtime.handlerUrl(element, 'problem_submit'),
        ans    = $(`#input_${shortModuleID(receiverB)}_2_1`)[0].value;

    $.ajax({
        type: "POST",
        url: handle,
        data: JSON.stringify({receiver: receiverB, answer: ans})
    });
});
