const electron = require("electron");
const {
  Menu,
  app,
  Tray,
  BrowserWindow,
  ipcMain: ipc,
  globalShortcut,
} = electron;
const exec = require("child_process").exec;
const child_process = require("child_process");
var { PythonShell } = require("python-shell");
const path = require("path");
var options = {};
function execute(command, callback) {
  exec(command, (error, stdout, stderr) => {
    callback(stdout);
  });
}
let tray = null;

options = {
  mode: "text",
  pythonPath:"D:/pythonProjects/TZAi/venv/scripts/python.exe",
};
var mode = "asst";
var manage = {
  state: -1,
  stateListener: function (val) {},
  set trigger(val) {
    this.state = val;
    this.stateListener(val);
  },
  get trigger() {
    return this.state;
  },
  registerListener: function (listener) {
    this.stateListener = listener;
  },
};

require("electron-reload")(__dirname, {
  electron: require(`${__dirname}/../node_modules/electron`),
});

var mainWindow = null;
app.on("ready", async (_) => {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 1000,
    resizeable: false,
    transparent: true,
    frame: false,
    fullscreen: true,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  globalShortcut.register("CommandOrControl+E", () => {
    mainWindow.show();
  });

  mainWindow.setResizable(true);
  mainWindow.setMenuBarVisibility(true);
  // mainWindow.setAlwaysOnTop(true);
  mainWindow.loadURL(`file://${__dirname}/index.html`);

  tray = new Tray(path.join(__dirname, "assets/tzai.png"));
  const contextMenu = Menu.buildFromTemplate([
    {
      label: "TZAI",
      click: function () {
        mainWindow.show();
      },
    },
    {
      label: "Quit",
      click: function () {
        mainWindow.quit();
        app.quit();
      },
    },
  ]);
  tray.on("click", () => {
    mode = "asst";
    manage.trigger += 1;
    mainWindow.show();
  });
  // tray.on("click", () => {
  //   mode="asst"
  //   manage.trigger+=1
  //   mainWindow.show();
  // });
  tray.setToolTip("TZAI - Your TZ Buddy");
  tray.setContextMenu(contextMenu);

  manage.registerListener(() => {
    console.log("CALLING SCRIPT");
    if (mode == "asst") {
      PythonShell.run(path.join(__dirname, "../ppl/bot.py"), options, function (
        //bot.py
        err,
        results
      ) {
        if (err) {
          throw err;
        }
        try {
          if (results.length > 3) {
            mainWindow.webContents.send("displayResponse", results); //event mirror isntance
          }
          console.log("results: ", results);
        } catch {
          //
        }
        manage.trigger += 1;
      });
    }
    if (mode == "chat") {
      PythonShell.run(
        path.join(__dirname, "../ppl/chat.py"),
        options,
        function (err, results) {
          if (err) throw err;
          try {
            if (results.length > 3) {
              mainWindow.webContents.send("displayResponse", results); //event mirror isntance
            }
            console.log("results: ", results);
          } catch {
            //
          }
          manage.trigger += 1;
        }
      );
    }
    if (mode == "sleep") {
      PythonShell.run(
        path.join(__dirname, "../ppl/sleep.py"),
        options,
        function (err, results) {
          if (err) throw err;
          try {
            if (results[0] == "activate") {
              mainWindow.show();
              mode = "asst";
              console.log("results: ", results);
            }
          } catch {
            //
          }
          manage.trigger += 1;
        }
      );
    }
  });
  manage.trigger += 1;

  // pyshell.on("message", function (message) {
  //   // received a message sent from the Python script (a simple "print" statement)
  //   console.log(message);
  // });

  mainWindow.on("closed", (_) => {
    mainWindow = null;
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.exit(0);
  }
});

ipc.on("startAsst", (evt) => {
  mode = "asst";
});
ipc.on("startChat", (evt) => {
  mode = "chat";
});

ipc.on("close", (evt) => {
  app.exit(0);
});
app.on("before-quit", () => {
  globalShortcut.unregisterAll();
  if (mainWindow) {
    mainWindow.removeAllListeners("close");
    mainWindow.close();
  }
});
ipc.on("min", (evt) => {
  mode = "sleep";
  mainWindow.hide();
});
