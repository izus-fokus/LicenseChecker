# LicenseChecker_frontend

## Introduction
License Checker is a comprehensive tool designed to assist engineers and researchers in identifying licenses for their open-source software. This application allows users to upload software code from Git repositories or from their local desktop to find available licenses within the code. Additionally, users can search for compatible licenses and view detailed information about individual licenses.

## Project Structure
This project consists of three main components:
1. **Backend Services**:
   - **License-Engine**: Responsible for analyzing the uploaded code and identifying the licenses present to find the compatible linceses.
   - **LicenseChecker**: Handles compatibility checks between different licenses and provides detailed information about each license.
2. **Frontend**:
    - A user-friendly interface for interacting with the backend services, uploading code, searching for licenses, and viewing compatibility information.

## Features
- **Upload Software Code**: Users can upload their software code from Git repositories or local files.
- **Identify Licenses**: Automatically detect and display licenses found in the uploaded code.
- **Find Compatible Licenses**: Search for licenses that are compatible with the detected licenses.
- **License Search**: Search for specific licenses by name.
- **Detailed License Information**: Access detailed information about individual licenses.


## Installation
### Backend Setup

1. **LicenseChecker**:

 
   - Navigate to the `LicenseChecker\api` directory:

   
     ```sh
     cd LicenseChecker\api
     ```
   - Install dependencies:
     ```sh
     npm install
     ```
   - Start the server:
     ```sh
     uvicorn main:app --reload
     ```

2. **License-Engine**:

  
     ```sh
     cd LicenseChecker\api
     ```
   - Install dependencies:
     ```sh
     npm install
     ```
   - Start the server:
     ```sh
     uvicorn main:app --reload
     ```

### Frontend Setup

   - Navigate to the `LicenseChecker_Frontend` directory:
     ```sh
     cd LicenseChecker_Frontend
     ```
   - Install dependencies:
     ```sh
     npm install
     ```
   - Start the server:
     ```sh
     npm run dev
     ```


## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
    1) Run `Extensions: Show Built-in Extensions` from VSCode's command palette
    2) Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

