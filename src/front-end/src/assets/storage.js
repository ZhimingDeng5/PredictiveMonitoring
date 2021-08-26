window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || 
                    window.msIndexedDB || window.shimIndexedDB;


window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || windows.msIDBTransaction;

window.IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange || window.maIDBKeyRange;

if(!window.indexedDB){
    alert("your browser is not support indexdb")
}

var db
var request = window.indexedDB.open("datastorage",1);

request.onerror = function(event){
    console.log("error"+event.target.result)
}

request.onsuccess = function(event){
    db = request.result
    console.log("success"+db)
}

request.onupgradeneeded= function(event){
    var db = event.target.result;
    var objectStore = db.createObjectStore("datastorage")
}