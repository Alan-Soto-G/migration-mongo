import { conectarMongo } from "./connect.js";
import mongoose from "mongoose";
import * as fs from "fs";
import * as path from "path";
import url from "url";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const entidadesDir = path.join(__dirname, "entidades");

(async () => {
    await conectarMongo();

    console.log("🧱 Creando base de datos y colecciones...");

    const archivos = fs.readdirSync(entidadesDir).filter(f => f.endsWith("_Mongoose.js"));

    for (const archivo of archivos) {
        const modulo = await import(`./entidades/${archivo}`);
        // Buscar el objeto que sea un modelo Mongoose válido
        const modelo = Object.values(modulo).find(
            (v) => v && v.collection && v.modelName
        );

        if (!modelo) {
            console.warn(`⚠️  No se encontró modelo válido en ${archivo}`);
            continue;
        }

        const nombre = modelo.collection.name;
        await mongoose.connection.createCollection(nombre);
        console.log(`✅ Colección creada: ${nombre}`);
    }

    console.log("🎉 Base de datos y colecciones listas en tu cluster.");
    process.exit(0);
})();
