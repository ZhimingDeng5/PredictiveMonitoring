import { Injectable } from '@angular/core';
declare var db: any
@Injectable({
  providedIn: 'root'
})
export class LocalStorageService {
  public Storagename = "datastorage";
  constructor() { }

  add(keyname, value) {
    return new Promise(async (resolve, reject) => {
      if (db != undefined) {
        const request = await db.transaction([this.Storagename], "readwrite").objectStore(this.Storagename).put(value, keyname);
        request.onsuccess = function (event) {
          if (event.target.result) {
            console.log("success")
            resolve("success")
          } else {
            console.log("error")
            resolve(false);
          }
        }
      }

    });






  }

  get(keyname) {
    return new Promise(async (resolve, reject) => {
      if (db != undefined) {
        const request = await db.transaction([this.Storagename], "readwrite").objectStore(this.Storagename).get(keyname);
        request.onsuccess = function (event) {
          if (event.target.result) {
            console.log("success")
            resolve(event.target.result)
          } else {
            console.log("error")
            resolve(false);
          }
        }
      }

    });

  }

  delete(keyname) {
    return new Promise(async (resolve, reject) => {
      if (db != undefined) {
        const request = await db.transaction([this.Storagename], "readwrite").objectStore(this.Storagename).delete(keyname);
        request.onsuccess = function (event) {
          if (event.target.result) {
            console.log("success")
            resolve("success")
          } else {
            console.log("error")
            resolve(false);
          }
        }
      }

    });

  }


}
