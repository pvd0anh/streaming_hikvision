// config/passport.js
var LocalStrategy   = require('passport-local').Strategy;
var User            = require('../app/models/user');

module.exports = function(passport) {

   passport.serializeUser(function(user, done) {
        done(null, user.id);
    });

    passport.deserializeUser(function(id, done) {
        //No use database, hard-code
        if (id===1){
            done(null, {
                'id' : id,
                'username' : 'admin',
                'password' : 'admin'
            })
        }
        else if (id ===2){
            done(null, {
                'id' : id,
                'username' : 'erman',
                'password' : 'erman@aioz'
            })
        }
        //User mongodb
        // User.findById(id, function(err, user) {
        //     done(err, user);
        // });
    });

   passport.use('local-login', new LocalStrategy({
        // by default, local strategy uses username and password, we will override with username
        usernameField : 'username',
        passwordField : 'password',
        passReqToCallback : true // allows us to pass back the entire request to the callback
    },
    function(req, username, password, done) { // callback with username and password from our form

        // find a user whose username is the same as the forms username
        // we are checking to see if the user trying to login already exists

        // User.findOne({ 'local.username' :  username }, function(err, user) {
        //     // if there are any errors, return the error before anything else
        //     if (err)
        //         return done(err);

        //     // if no user is found, return the message
        //     if (!user)
        //         return done(null, false, req.flash('loginMessage', 'No user found.')); // req.flash is the way to set flashdata using connect-flash

        //     // if the user is found but the password is wrong
        //     if (!user.validPassword(password))
        //         return done(null, false, req.flash('loginMessage', 'Wrong password.')); // create the loginMessage and save it to session as flashdata

        //     if(!user.isActive())
        //         return done(null, false, req.flash('loginMessage', 'Account is not active')); // create the loginMessage and save it to session as flashdata
            
        //     // all is well, return successful user
        //     return done(null, user);
        // });
        
        if ((username === 'admin' && password === 'admin') || (username === 'erman' && password === 'erman@aioz')){
            if(username === 'admin'){
                id = 1;
            }
            else if(username === 'erman'){
                id = 2;
            }
            var user = {
                'id' : id,
                'username' : username,
                'password' : passport
            }
            return done(null, user);
        }
        else{
            return done(null, false, req.flash('loginMessage', 'No user found or wrong password.'));
        }

    }));

    passport.use('local-signup', new LocalStrategy({
        usernameField : 'username',
        passwordField : 'password',
        passReqToCallback : true 
    },
    function(req, username, password, done) {
        process.nextTick(function() {
        User.findOne({ 'local.username' :  username }, function(err, user) {
            if (err)
                return done(err);
            if (user) {
                return done(null, false, req.flash('signupMessage', 'The username already exists. Please use a different username.'));
            } else {
                var newUser            = new User();
                newUser.local.username = username;
                newUser.local.password = newUser.generateHash(password);
                newUser.local.isActive = true;
                newUser.save(function(err) {
                    if (err)
                        throw err;
                    return done(null, newUser);
                });
            }

        });    

        });

    }));
};