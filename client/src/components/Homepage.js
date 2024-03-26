import React, { useEffect, useState } from "react";
import { NavLink, useHistory } from "react-router-dom/cjs/react-router-dom.min";
import Header from "./Header";
import Video from "../css/background.mp4"

function Homepage({ fillGameData, loggedInUser, logoutUser }) {
    const history = useHistory()
    function handleClick(e) {
        history.push("/play")
    }

    return (
        <>
            <Header loggedInUser={loggedInUser} logoutUser={logoutUser} />
            <div id="homepage-container">
                <div id="first-container">
                    <video autoPlay loop muted playsInline>
                        <source src={Video} type="video/mp4"></source>
                    </video>
                    <h1 id="slogan">TAKE THE RISK</h1>
                    <button onClick={handleClick} id="play-button">PLAY NOW</button>
                </div>
                <h1 className="headings">WHAT WE OFFER</h1>
                <div id="second-container">
                    <section className="section" id="section1">
                        <div class="section-image" id="first-img"></div>
                        <div class="section-content" id="first-content-container">
                            <h2>IMMERSIVE COMPETITION</h2>
                            <div id="first-paragraph">
                                <p>Immerse yourself in a competitive environment where every move counts, offering a thrilling experience that challenges your skills and strategies.</p>
                            </div>
                        </div>
                    </section>
                    <section className="section" id="section2">
                        <div class="section-content" id="second-content-container">
                            <h2>VIRTUAL POKER EXPERIENCE</h2>
                            <div id="second-paragraph">
                                <p>Embark on a virtual journey into the world of poker, where you can hone your card-playing prowess and engage in intense matches with players from around the globe, all from the comfort of your home.</p>
                            </div>
                        </div>
                        <div class="section-image" id="second-img"></div>
                    </section>
                    <section className="section" id="section3">
                        <div class="section-image" id="third-img"></div>
                        <div class="section-content" id="third-content-container">
                            <h2>CLIENT FRIENDLY</h2>
                            <div id="third-paragraph">
                                <p>Designed with the needs of our clients in mind, our platform ensures a user-friendly experience, offering intuitive interfaces and seamless interactions to enhance satisfaction and usability.</p>
                            </div>
                        </div>
                    </section>
                </div>
                <h1 className="headings">OUR TOP EARNERS</h1>
                <div id="third-container">
                    <section className="third-container-section" id="third-container-section1">
                        <div className="earner-name" id="earner-name1">
                            Eman Gurung
                        </div>
                        <div className="earnings">
                        $10M+
                        </div> 
                        <p className="quote">
                            "I wasn't really into poker or anything, but I needed some way to fund my day to day expenses. Thanks to the help of <b>Premium Poker</b>, I'm able to afford food for my family, go out on trips, and live freely. Without the help of <b>Premium Poker</b>, I would be in the midst of applying for the military." - Eman Gurung
                        </p>
                    </section>
                    <section className="third-container-section" id="third-container-section2">
                        <div className="earner-name" id="earner-name2">
                            Sergio Heredia
                        </div>
                        <div className="earnings">
                          $100M+
                        </div>
                        <p className="quote">
                            "I always loved gambling since I was little, but my addiction resulted in getting suspended from numerous casinos. However, <b>Premium Poker</b> has allowed me to continue that love and earn honest money. Without <b>Premium Poker</b>, my life would be incomplete. I'm appreciative for the developers who has saved me and countless others." - Sergio Heredia
                        </p>
                    </section>
                    <section className="third-container-section" id="third-container-section3">
                        <div className="earner-name" id="earner-name2">
                            Ava Grace
                        </div>
                        <div className="earnings">
                            $50M+
                        </div>
                        <p class="quote">
                            "I was a broke college student. I didn't have any money to fund my classes, and provide myself meals through out the day. That's when I found <b>Premium Poker</b>, I was a little hesitant at first because it looked so complicated for my small brain, but as I learned through playing, I started winning! I now can attend classes comfortable, and not worry about my next meal, thanks for <b>Premium Poker</b>." - Ava Grace
                        </p>
                    </section>
                </div>
                <div id="fourth-container">
                <h1 className="headings">ABOUT US</h1>
                    <div id="about-container">
                        <div className="about-containers" id="first-about-container">
                            <div id="first-about-caption">Welcome to Premium Poker, where excitement meets sophistication in the virtual realm of card games. At Premium Poker, we pride ourselves on offering an unparalleled online poker experience that combines cutting-edge technology with a passion for the game. Our platform provides players with a seamless interface, stunning graphics, and a wide variety of game options to suit every skill level and preference. Whether you're a seasoned pro or a novice looking to hone your skills, Premium Poker is the ultimate destination for thrilling gameplay and endless entertainment. Join us today and discover why discerning players choose Premium Poker for the most immersive and rewarding online poker experience available.</div>
                            <div id="first-about-image"></div>
                        </div>
                        <div className="about-containers" id="second-about-container">
                            <div id="second-about-caption-container">
                                <div id="second-about-header-caption">
                                    PLAY VIRTUAL ONLINE POKER
                                </div>
                                <div id="second-about-caption">                            
At Premium Poker, we hold our users in the highest regard, recognizing that they are the heartbeat of our platform. We deeply value the trust and loyalty they place in us, and it is our unwavering commitment to ensuring their satisfaction and enjoyment that drives everything we do. From providing responsive customer support to continuously enhancing our platform based on user feedback, we prioritize the needs and preferences of our community above all else. Every feature, every update, and every interaction is guided by our dedication to delivering an exceptional experience that exceeds expectations. At Premium Poker, our users aren't just players – they're valued members of our family, and their happiness and fulfillment are at the core of our mission.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="fifth-container">
        
                    <div id="columns">
                        <div className="column" id="first-column">
                            <h5 id="heavy-header">QUICK LINKS</h5>
                            <h5>HOME</h5>
                            <h5>SIGN-UP OFFERS</h5>
                            <h5>HOUSE RULES</h5>
                            <h5>HANDBOOK</h5>
                            <h5 id="heavy-header">GAMES</h5>
                            <h5>POKER GAMES</h5>
                        </div>
                        <div className="column" id="first-column">
                            <h5 id="heavy-header">ADDITIONAL INFORMATION</h5>
                            <h5>ABOUT</h5>
                            <h5>WHAT ARE POINTS</h5>
                            <h5>RELEASE NOTES</h5>
                            <h5>PLAY FOR FREE</h5>
                            <h5>POKER DICTIONARY</h5>
                            <h5>RESPONSIBLE SOCIAL GAMEPLAY</h5>

                        </div>
                        <div className="column" id="first-column">
                            <h5 id="heavy-header">SUPPORT</h5>
                            <h5>WHAT ARE ICONS</h5>
                            <h5>WHAT ARE TAGS</h5>
                            <h5>INVENTORY DETAILS</h5>
                            <h5>STORE DETAILS</h5>
                            <h5 id="heavy-header">LEGAL REGULATIONS</h5>
                            <h5>TERMS AND CONDITIONS</h5>
                        </div>

                    </div>
                </div>
            </div>
        </>
    );
}

export default Homepage;
