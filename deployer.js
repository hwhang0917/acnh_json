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
  if (err) {
    console.log(`❌ Failed to deploy to GitHub Pages! ${err}`);
  } else {
    console.log(`✅ Deployed to https://hwhang0917.github.io/acnh_json/`);
  }
});
