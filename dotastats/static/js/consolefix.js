// http://snippets.dzone.com/posts/show/6326

if (! ("console" in window) || !("firebug" in console)) {
 var names = ["log", "debug", "info", "warn", "error", "assert", "dir", "dirxml", "group"
 , "groupEnd", "time", "timeEnd", "count", "trace", "profile", "profileEnd"];
 window.console = {};
 var EmptyFn = function() {};
 for (var i = 0; i <names.length; ++i) window.console[names[i]] = EmptyFn;
}
