import { Streamlit, RenderData } from "streamlit-component-lib"
import {Clerk} from "@clerk/clerk-js";
const clerkPubKey = "pk_test_cHJpbWUtc2hyaW1wLTQwLmNsZXJrLmFjY291bnRzLmRldiQ" ;

// Add text and a button to the DOM. (You could also add these directly
// to index.html.)
const clerk = new Clerk(clerkPubKey);
await clerk.load();

//app.setAttribute("id","app")


// Add a click handler to our button. It will send data back to Streamlit.
// let numClicks = 0
// let isFocused = false
// console.log("XXX")
// button.onclick = function(): void {
//   // Increment numClicks, and pass the new value back to
//   // Streamlit via `Streamlit.setComponentValue`.
//   numClicks += 1
//   Streamlit.setComponentValue(numClicks)
// }
//
// button.onfocus = function(): void {
//   isFocused = true
// }
//
// button.onblur = function(): void {
//   isFocused = false
// }

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
var current_data = null
function compare_objs(obj1,obj2){
    const diffs = []
    for ( let it of Object.entries(obj2)){
        if (obj1[it[0]] !== it[1]){
            diffs.push(it[0],it[1],obj1[it[0]])
        }
    }
    return diffs
}
async function extract_data(listener){
    if (listener && listener.user) {
        var data = {
            firstName: listener.user.firstName,
            lastName: listener.user.lastName,
            fullName: listener.user.fullName,

            id: listener.user.id,
            imageUrl: listener.user.imageUrl
        }
        if (listener.session) {
            data.status = listener.session.status
            data.session_id = listener.session.id
            data.expiresAt = listener.session.expireAt
            data.createdAt = listener.session.createdAt
            listener.session.getToken().then(
                function (token) {
                    data.token = token;

                    send_data(data);
                    return data
                }
            )
        }
        return data
    }
}
function send_data(data){
    if (!data){return}
    let diffs=[]
    if(current_data){
        diffs = compare_objs(current_data,data)
    } else{
        diffs.push("all")
    }
    if (diffs.length){
        console.log(diffs)
        current_data = Object.assign({},data)
        Streamlit.setComponentValue(data)

    }

}
function onRender(event ) {
    // Get the RenderData from the event
    const data = (event).detail
    if (clerk.user) {
        extract_data(clerk) .then((data)=>send_data(data))
        const userButtonDiv =
            document.getElementById("user-button");
        clerk.mountUserButton(userButtonDiv);
    } else {
        const signInDiv =
            document.getElementById("sign-in");

        clerk.mountSignIn(signInDiv);
    }
    if (data.theme) {

    }
  Streamlit.setFrameHeight()
}



clerk.addListener(async function addListener(listener ){
    let data  = await extract_data(listener)
    if (data){
        send_data(data);
    }
 })

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight()
