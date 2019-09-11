// app/routes.js
module.exports = function(app, passport) {

    // =====================================
    // Trang chủ (có các url login) ========
    // =====================================
    app.get('/', isLoggedIn, function(req, res) {
        res.render('index.ejs'); // 
    });

    // =====================================
    // Đăng nhập ===============================
    // =====================================
    // hiển thị form đăng nhập
    app.get('/login', function(req, res) {
        res.render('login.ejs', { message: req.flash('loginMessage') }); 
    });
    
   app.post('/login', passport.authenticate('local-login', {
        successRedirect : '/',
        failureRedirect : '/login', 
        failureFlash : true
    }));

//     // =====================================
//     // Đăng ký ==============================
//     // =====================================
//     // hiển thị form đăng ký
//     app.get('/signup', function(req, res) {
//         res.render('signup.ejs', { message: req.flash('signupMessage') });
//     });

//     // Xử lý form đăng ký ở đây
//    app.post('/signup', passport.authenticate('local-signup', {
//         successRedirect : '/', // Điều hướng tới trang hiển thị profile
//         failureRedirect : '/signup', // Trở lại trang đăng ký nếu lỗi
//         failureFlash : true 
//     }));

//     // =====================================
//     // Thông tin user đăng ký =====================
//     // =====================================
//     app.get('/profile', isLoggedIn, function(req, res) {
//         res.render('profile.ejs', {
//             user : req.user // truyền đối tượng user cho profile.ejs để hiển thị lên view
//         });
//     });

    // =====================================
    // Đăng xuất ==============================
    // =====================================
    app.get('/logout', function(req, res) {
        req.logout();
        res.redirect('/');
    });
};

// Hàm được sử dụng để kiểm tra đã login hay chưa
function isLoggedIn(req, res, next) {
    if (req.isAuthenticated())
        return next();
    res.redirect('/login');
}