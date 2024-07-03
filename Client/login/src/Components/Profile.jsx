import React, { useContext, useRef, useState, useEffect} from "react";
import Topbar from "./Topbar.jsx";
import "./Profile.css"
import profileimage from './Innovature Wallpaper.png'
import { AuthContext } from "../AuthContext.jsx"; 
import { useCookies,Cookies } from "react-cookie";
import axios from "axios";

const Profile = () => {

    const [cookies, setCookie, removeCookie] = useCookies(['user'])
    const [profileData, setProfileData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        birthday: ''
    });
    const [email, setEmail] = useState('')
    
    // useEffect(() => {
        //     const fetchEmail = async (usernam) => {
            //         try {
                //             // Fetch email based on username
                //             const response = await axios.post(`http://127.0.0.1:8000/authentication/get_user_email/`, {usernam: usernam});
                //             console.log("response email "+response.data.email)
                //             setEmail(response.data.email) ;
                //         } catch (error) {   
                    //             console.error('Error fetching email:', error);
                    //             return ''; // Return empty string or handle error appropriately
                    //         }
                    //     }
                    //         fetchEmail(usernamefromCookie)
                    // },[]);
                    
                    useEffect(() => {
                        // Fetch the profile data from the backend
                        async function fetchProfile(usernam) {
                            try {
                                console.log("hello"+usernam)
                                const response = await axios.post(`http://127.0.0.1:8000/authentication/get_user_profile/`, {usernam: usernam});
                                console.log("ivide")
                                console.log("responsive profile "+response.data.username)
                                // const data = await response.json();
                                setProfileData(response.data); // Update profileData state with fetched data
                            } catch (error) {
                                console.log("ivide error")
                                console.error('Error fetching profile:', error);
                            }
                        }
                        const usernamefromCookie = cookies.user
                        fetchProfile(usernamefromCookie);
                    }, []);
        // Function to handle input changes
        const handleInputChange = (e) => {
            const { name, value } = e.target;
            setProfileData({ ...profileData, [name]: value });
        };
    
        // Function to handle form submission
        const handleSubmit = (e) => {
            e.preventDefault();
            // Logic to handle form submission (e.g., send data to server)
            console.log("Submitted:", profileData);
        };
    return (
      <div>
        <Topbar logotext="Profile"/>
        <div className="p-container">
            <div className="img-cont">
                <img className="profile-image" src={profileimage} alt="Profile" />  
            </div> 
        <div className="profile-content">
                    <h2>Profile Information</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <input
                                type="text"
                                className="input-box"
                                id="inputUsername"
                                name="username"
                                value={profileData.username}
                                onChange={handleInputChange}
                                //readOnly
                            />
                        </div>
                        <div className="mb-3">
                            <input
                                placeholder="First Name"
                                type="text"
                                className="input-box"
                                id="inputFirstName"
                                name="firstName"
                                value={profileData.first_name}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="mb-3">
                            <input
                                placeholder="Last name"
                                type="text"
                                className="input-box"
                                id="inputLastName"
                                name="lastName"
                                value={profileData.last_name}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="mb-3">
                            <input
                                placeholder="E-mail"
                                type="email"
                                className="input-box"
                                id="inputEmail"
                                name="email"
                                value={profileData.email}
                                onChange={handleInputChange}
                                //readOnly    
                            />
                        </div>
                        <div className="mb-3">
                            <input
                                placeholder="Phone Number"
                                type="tel"
                                className="input-box"
                                id="inputPhone"
                                name="phone"
                                value={profileData.phone}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="mb-3">
                            <input
                            placeholder="Birthday"
                                type="date"
                                className="input-box"
                                id="inputBirthday"
                                name="birthday"
                                value={profileData.birthday}
                                onChange={handleInputChange}
                            />
                        </div>
                        <button type="submit" className="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Profile;