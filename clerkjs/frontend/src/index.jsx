import { Streamlit, RenderData } from "streamlit-component-lib"
import {Clerk} from "@clerk/clerk-js";
const clerkPubKey = "pk_test_cHJpbWUtc2hyaW1wLTQwLmNsZXJrLmFjY291bnRzLmRldiQ" ;

// Add text and a button to the DOM. (You could also add these directly
// to index.html.)
var clerk = null;

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
            data.token = await listener.session.getToken({template : 'default'})


        }
        send_data(data)
        return data
    } else if (listener?.client){
        const signInDiv =
            document.getElementById("sign-in");

        clerk.mountSignIn(signInDiv);
        return {status:'No session'}
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
        current_data = Object.assign({},data)
        Streamlit.setComponentValue(data)

    }

}
async function onRender(event ) {
    const data = (event).detail

    if (!clerk){
        let clerkPubKey = data.clerkPubKey
        clerk = new Clerk(clerkPubKey);
        await clerk.load();
        clerk.addListener(async function addListener(listener ){
            let data  = await extract_data(listener)
            if (data){
                send_data(data);
            }
        })
    }
    let userdata = await extract_data(clerk)
    if (userdata){
        send_data(userdata);
    }
    // Get the RenderData from the event
    if (clerk.user ) {
        const userButtonDiv =
            document.getElementById("user-button");
        //clerk.redirectToSignIn({signInForceRedirectUrl:"javascript:void(0)"})
        clerk.mountUserButton(userButtonDiv,{showName:true,userProfileMode:"modal",afterSignOutUrl:"javascript:void(0)"});
    } else {
        const signInDiv =
            document.getElementById("sign-in");

        clerk.mountSignIn(signInDiv);
    }


    if (data.theme) {

    }
  Streamlit.setFrameHeight()
}





Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight()
