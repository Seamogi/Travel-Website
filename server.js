const express = require('express');
const session = require('express-session');
const { Issuer, generators } = require('openid-client');
const app = express();
const bodyParser  = require('body-parser');

const axios = require('axios');

app.use(bodyParser.urlencoded());

app.use(express.static('public'));

app.set('view engine', 'ejs');

// Code to connect to the AWS cognito configuration and set up the redirect URL after login
let client;
async function initializeClient() {
    const issuer = await Issuer.discover('https://cognito-idp.us-east-1.amazonaws.com/us-east-1_W9e55lCun');
    client = new issuer.Client({
        client_id: '4c2ukjsnde24bok70eao19k1jo',
        client_secret: '1ui8kfv18gc76e1oe3lnes0v0cdca3ebdl5vfli8coce4q6eg31l',
        redirect_uris: ['http://localhost:8080/callback'],
        response_types: ['code']
    });
};
initializeClient().catch(console.error);

app.use(session({
    secret: 'some secret',
    resave: false,
    saveUninitialized: false
}));

// Code to make every ejs page have the isAuthenticated variable to see if the user is logged in or not.
app.use((req, res, next) => {
    app.locals.isAuthenticated = req.session.userInfo ? true : false;
    app.locals.userInfo = req.session.userInfo || null;
    next();
});

// Create the frontend path for the home page.
app.get('/', (req, res) => {
    res.render('index.ejs', {
    });
});

// Create the frontend path for the AWS cognito login page and redirect user after login
app.get('/login', (req, res) => {
    const nonce = generators.nonce();
    const state = generators.state();

    req.session.nonce = nonce;
    req.session.state = state;

    const authUrl = client.authorizationUrl({
        scope: 'email openid profile',
        state: state,
        nonce: nonce,
    });

    res.redirect(authUrl);
});


// Create the path that the login page goes to after successful login and creates the variable to store the user's information. Also contains the redirect path.
app.get('/callback', async (req, res) => {
    try {
        const params = client.callbackParams(req);
        const tokenSet = await client.callback(
            'http://localhost:8080/callback',
            params,
            {
                nonce: req.session.nonce,
                state: req.session.state
            }
        );

        const userInfo = await client.userinfo(tokenSet.access_token);
        req.session.userInfo = userInfo;

        const response = await axios.post('http://localhost:5000/callback', {
            first_name: userInfo.given_name, 
            last_name: userInfo.family_name,
            email: userInfo.email
        });

        res.redirect('/');
    } catch (err) {
        console.error('Callback error:', err);
        res.redirect('/');
    }
});


// Create the path to log out a user by destroying the session. Also redirects user back to the homepage.
app.get('/logout', (req, res) => {
    req.session.destroy();
    const logoutUrl = `https://us-east-1w9e55lcun.auth.us-east-1.amazoncognito.com/logout?client_id=4c2ukjsnde24bok70eao19k1jo&logout_uri=http://localhost:8080/`;
    res.redirect(logoutUrl);
});


// Create the frontend path for destination weddings page.
app.get('/destination-weddings', function(req, res) {
    res.render("destination-weddings.ejs", {
    });
});

// Create the frontend path for the group travel services page.
app.get('/group-travel-services', function(req, res) {
    res.render("group-travel-services.ejs", {
    });
});

// Create the frontend path for the excursions page.
app.get('/excursions', function(req, res) {
    res.render("excursions.ejs", {
    });
});

// Create a function that checks whether the user is logged in. If user is logged in, the function continues. 
// If user is not logged in, user is redirected back to the login page.
function isAuthenticated(req, res, next) {
    if (req.session.userInfo) {
        return next();
    } else {
        res.redirect('/login');
    }
}

// Create the frontend path for the travel inquiry form page which checks if the user is logged in.
app.get('/travel-inquiry-form', isAuthenticated, async (req, res) => {
    res.render('travel-inquiry-form', {
        userInfo: req.session.userInfo
    })
});

// Create the frontend path for the travel inquiry form page which can only be accessed if the user is not logged in.
app.get('/travelinquiryformnoaccess', async (req, res) => {
    res.render('travelinquiryformnoaccess')
});

// Create the frontend path for the terms of service page.
app.get('/terms-of-service', (req, res) => {
    res.render('terms-of-service');
});

// Create the frontend path for the privacy policy page.
app.get('/privacy-policy', (req, res) => {
    res.render('privacy-policy'); 
});

// Create the frontend path for the contact us page which checks if the user is logged in.
app.get('/contact', isAuthenticated, async (req, res) => {
    res.render('contact', {
        userInfo: req.session.userInfo
    });
});

// Create the frontend path for the contact us page which can only be accessed if the user is not logged in.
app.get('/contactnoaccess', async (req, res) => {
    res.render('contactnoaccess');
});

// localhost:8080 is the URL
app.listen(8080);
console.log('Listening on port 8080. Server is http://localhost:8080');