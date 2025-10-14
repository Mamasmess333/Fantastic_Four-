import express from "express";
import path from "path";
import { fileURLToPath } from "url";

export function createApp() {
  const app = express();

  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);

  app.use(express.static(path.join(__dirname, "public")));

  app.get("/api", (req, res) => {
    res.json({ message: "Hello from Express + Mongoose!" });
  });

  return app;
}


// import express from "express";
// import path from "path";
// import { fileURLToPath } from "url";

// export function createApp() {
//   const app = express();

//   // Needed to resolve __dirname in ESM
//   const __filename = fileURLToPath(import.meta.url);
//   const __dirname = path.dirname(__filename);

//   // Serve static files
//   app.use(express.static(path.join(__dirname, "public")));

//   // Example route
//   app.get("/api", (req, res) => {
//     res.json({ message: "Hello from Express + Mongoose!" });
//   });

//   return app;
// }