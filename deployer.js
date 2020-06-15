var ghpages = require("gh-pages");

var options = {
  branch: "master",
  repo: "https://github.com/hwhang0917/acnh_json.git",
  message: "Updated: Auto-pushed via gh-pages",
  user: {
    name: "hwhang0917",
    email: "hwhang0917@gmail.com",
  },
};

ghpages.publish("dist", options, (err) => {
  console.log(`❌ Failed to deploy to GitHub Pages! ${err}`);
});
