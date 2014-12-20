(function(){
    var app = angular.module('socialLite', []);

    app.controller('EventController',['$http', '$log', '$rootScope', function($http, $log, $scope, $rootScope){
//        this.eventItems = events;

        var eventCtrl = this;
        eventCtrl.eventItems = [];
        eventCtrl.newEvent = {
            category: []
        };
        eventCtrl.eventDetail = {
            member:[]
        };
        eventCtrl.allInts = all_interests;
        eventCtrl.msg = "";
        eventCtrl.rsvp = false;
        eventCtrl.discussion = [];
        eventCtrl.newPost = {};
        eventCtrl.rsvpmsg = "";

        $http.get('/all-events').success(function(data){
            eventCtrl.eventItems = data;
        });

        $http.get('/getEventDetail').success(function(data){
            eventCtrl.eventDetail = data;
            if(typeof eventCtrl.eventDetail.eventid != "undefined"){
                $http.get('/getDiscussion').success(function(data){
                    eventCtrl.discussion = data;
                });
            }
        });

//        $http.get('/all-interests').success(function(data){
//            eventCtrl.allInts = data;
//        });

        eventCtrl.createNewEvent = function(){
            if(eventCtrl.msg.length > 0){
                eventCtrl.msg.length = "";
            }
            $http.post('/createNewEvent', eventCtrl.newEvent).success(function(data){
                // do something?
                eventCtrl.newEvent = {category: []};
                eventCtrl.msg = "Success!";
            });
        };

        eventCtrl.gotoEventDetail = function(eventid){
            $http.post('/eventDetail',eventid).success(function(data){
                debugger;
            });
        };

        $scope.gotoEventDetail = function(eventid){
            $http.post('/eventDetail',eventid).success(function(data){
                debugger;
            });
        }

        eventCtrl.rsvpEvent = function(){
            if(eventCtrl.rsvpmsg.length > 0){
                eventCtrl.rsvpmsg = "";
            }
            $http.post('/rsvpEvent','true').success(function(data){
                eventCtrl.rsvpmsg = "Success!";
                eventCtrl.rsvpflag = true;
                debugger;
            });
        };

        eventCtrl.postNewDiscussion = function(){
            eventCtrl.newPost.creator = $scope.currentUserName;
            eventCtrl.discussion.push(eventCtrl.newPost);
            $http.post('/newPost', eventCtrl.newPost).success(function(data){
                debugger;
            });
            eventCtrl.newPost = {};
        };

//        eventCtrl.checkRSVPed = function(user){
//            if(event_details.member.indexOf(user) > 0){
//                return true;
//            }
//            else{
//                return false;
//            }
//        }
        $scope.$on('$viewContentLoaded', jq_Controls());
    }]);

    app.controller('UserController', ['$http', '$log', '$rootScope', 'fileUpload', function ($http, $log, $scope, fileUpload) {

        var userCtrl = this;
        userCtrl.currentUser = {};
        userCtrl.allInts = all_interests;
        userCtrl.rsvpedEvent = [];
        userCtrl.reco = [];
        userCtrl.auth = {};
        userCtrl.msg = "";

        $scope.uploadFile = function(){
        var file = $scope.myFile;
        console.log('file is ' + JSON.stringify(file));
        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };

        $http.get('/currentUserInfo').success(function (data) {
            userCtrl.currentUser = data;
            if(typeof userCtrl.currentUser.username != "undefined"){
                $scope.currentUserName = userCtrl.currentUser.username;
            }
        });

//        $http.get('/all-interests').success(function(data){
//            userCtrl.allInts = data;
//        });

        userCtrl.updateUserInfo = function(){
            if(userCtrl.msg.length>0){
                userCtrl.msg = "";
            }
            $http.post('/updateCurrentUser', userCtrl.currentUser).success(function(data){
                // do something?
                userCtrl.msg="Success!";
            });
        };

        userCtrl.checkUser = function(){
            if(typeof userCtrl.currentUser['username'] != 'undefined')
            {
                return true;
            }
            else{
                return false;
            }
        };

        userCtrl.login = function(){
            if(userCtrl.msg.length > 0){
                userCtrl.msg = "";
            }
            $http.post('/login', userCtrl.auth).success(function(data){
                userCtrl.msg = "Success!";
                userCtrl.auth = {};
            });
        };

        userCtrl.signup = function(){
            if(userCtrl.msg.length > 0){
                userCtrl.msg = "";
            }
            $http.post('/signup', userCtrl.auth).success(function(data){
                userCtrl.msg = "Success!";
                userCtrl.auth = {};
            });
        }

        userCtrl.logout = function(){
            $http.post('/logout', "");
            userCtrl.currentUser = {};
        };

    }]);

    app.controller("AccountController", ['$http', '$log','$rootScope', function($http, $log, $scope, $rootScope){
        var accCtrl = this;
        accCtrl.rsvpedEvent = [];
        accCtrl.reco = [];

        $http.get('/getRsvpedEvent').success(function(data){
            accCtrl.rsvpedEvent = data;
        });

        $http.get('/getReco').success(function(data){
            accCtrl.reco = data;
        });
    }]);

    app.filter('getCatedInts', function () {
      return function (items, cate) {
        var filtered = [];
        for (var i = 0; i < items.length; i++) {
          var item = items[i];
          if (item.parent === cate) {
            filtered.push(item);
          }
        }
        return filtered;
      };
    });

    var currentUserInfo = {
        userid: "100001userid",
        password: "test password",
        displayname: "test user displayname",
        email_address: "huangbq.01@gmail.com",
        location: "college park, MD",
        age: "25",
        gender: "male",
        bio: "I'm interested in everything! I'm a test user!",
        interests: [{
            name: "Social Media",
            parent: "Internet & Technology"
        },
        {
            name: "Interaction Design",
            parent: "Internet & Technology"
        },
        {
            name: "Cloud Computing",
            parent: "Internet & Technology"
        }],
        facebook_url: "www.facebook.com/test-user-facebook",
        twitter_url: "www.twitter.com/test-user-twitter"
    };

    var events = [
        {
        name: "DC wine hangout",
        thumbnail: "img/1.jpg",
        caption: "The wine Caption"
    },{
        name: "DC game hangout",
        thumbnail: "img/2.jpg",
        caption: "The game strings"
    },{
        name: "Maryland football meetup",
        thumbnail: "img/3.jpg",
        caption: "football YESSSS!"
    },{
        name: "Maryland basketball meetup",
        thumbnail: "img/4.jpg",
        caption: "GET A DUNK!"
    }
    ];

//    var all_interests = [
//        {
//            name: "Art",
//            parent: "Arts & Entertainment"
//        },
//        {
//            name: "Fiction",
//            parent: "Arts & Entertainment"
//        },
//        {
//            name: "Film",
//            parent: "Arts & Entertainment"
//        },
//        {
//            name: "Lean Startup",
//            parent: "Business & Career"
//        },
//        {
//            name: "Marketing",
//            parent: "Business & Career"
//        },
//        {
//            name: "Investing",
//            parent: "Business & Career"
//        },
//        {
//            name: "Social Media",
//            parent: "Internet & Technology"
//        },
//        {
//            name: "Interaction Design",
//            parent: "Internet & Technology"
//        },
//        {
//            name: "Cloud Computing",
//            parent: "Internet & Technology"
//        }
//    ];

    var all_interests=[
        {parent_c:"Social", children_c:["Nightlife","Fun Times"]},
        {parent_c:"Internet & Technology", children_c:["Hacking", "Programming", "Java", "Photography", "PHP", "Social Media", "Interaction Design", "Cloud Computing"]},
        {parent_c:"Hobbies", children_c:["Beer", "Travel", "Wine", "Games", "Motorcycle Riding"]},
        {parent_c:"Science", children_c:["Evolution", "Astronomy", "Biology", "Innovation"]},
        {parent_c:"Health & Support", children_c:["Meditation", "Yoga", "Depression", "Fitness"]},
        {parent_c:"Sport", children_c:["Football", "Swimming"]},
        {parent_c:"Arts & Entertainment", children_c:["Art", "Fiction", "Film"]},
        {parent_c:"Business & Career", children_c:["Lean Startup", "Marketing", "Investing"]}
    ];

    var event_details = {
        eventid: "123123",
        name: "Empowering Mobile Development with Angular",
        location: "123 Test Rd, college park, MD",
        description: 'A discussion of some of the core technologies we use at Nudge to enable Angular-based JS/HTML5 applications to "feel native", including PhoneGap/Cordova, ngTouch, and "notifying" promises with local data for lightning-fast response times. The talk should hopefully be useful to anyone interested in pursuing PhoneGap apps, mobile web development, and anyone looking to make their Angular apps feel more responsive.'
    };

    var attender_list = {
        eventid : "123123",
        attenders: [{
            userid: "100001userid",
            name: "test user"
        },
        {
            userid: "100002userid",
            name: "test user2"
        },{
            userid: "100003userid",
            name: "test user3"
        }]
    };

    app.directive('fileModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;

                element.bind('change', function(){
                    scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
    }]);

    app.service('fileUpload', ['$http', function ($http) {
        this.uploadFileToUrl = function(file, uploadUrl){
            var fd = new FormData();
            fd.append('file', file);
            $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
            .success(function(){
            })
            .error(function(){
            });
        }
    }]);

    app.directive('checklistModel', ['$parse', '$compile', function($parse, $compile) {
      // contains
      function contains(arr, item) {
        if (angular.isArray(arr)) {
          for (var i = 0; i < arr.length; i++) {
            if (angular.equals(arr[i], item)) {
              return true;
            }
          }
        }
        return false;
      }

      // add
      function add(arr, item) {
        arr = angular.isArray(arr) ? arr : [];
        for (var i = 0; i < arr.length; i++) {
          if (angular.equals(arr[i], item)) {
            return arr;
          }
        }
        arr.push(item);
        return arr;
      }

      // remove
      function remove(arr, item) {
        if (angular.isArray(arr)) {
          for (var i = 0; i < arr.length; i++) {
            if (angular.equals(arr[i], item)) {
              arr.splice(i, 1);
              break;
            }
          }
        }
        return arr;
      }

      function postLinkFn(scope, elem, attrs) {
        // compile with `ng-model` pointing to `checked`
        $compile(elem)(scope);

        // getter / setter for original model
        var getter = $parse(attrs.checklistModel);
        var setter = getter.assign;

        // value added to list
        var value = $parse(attrs.checklistValue)(scope.$parent);

        // watch UI checked change
        scope.$watch('checked', function(newValue, oldValue) {
          if (newValue === oldValue) {
            return;
          }
          var current = getter(scope.$parent);
          if (newValue === true) {
            setter(scope.$parent, add(current, value));
          } else {
            setter(scope.$parent, remove(current, value));
          }
        });

        // watch original model change
        scope.$parent.$watch(attrs.checklistModel, function(newArr, oldArr) {
          scope.checked = contains(newArr, value);
        }, true);
      }

      return {
        restrict: 'A',
        priority: 1000,
        terminal: true,
        scope: true,
        compile: function(tElement, tAttrs) {
          if (tElement[0].tagName !== 'INPUT' || !tElement.attr('type', 'checkbox')) {
            throw 'checklist-model should be applied to `input[type="checkbox"]`.';
          }

          if (!tAttrs.checklistValue) {
            throw 'You should provide `checklist-value`.';
          }

          // exclude recursion
          tElement.removeAttr('checklist-model');

          // local scope var storing individual checkbox model
          tElement.attr('ng-model', 'checked');

          return postLinkFn;
        }
      };
    }]);
}());