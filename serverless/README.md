# Demo app for serverless with Vercel

This is a demo app for serverless with Vercel.

## How to use

After setting up your Vercel account, the next step is to deploy a serverless function. Here's a step-by-step guide on how to do it:

- First, install the Vercel CLI (Command Line Interface) on your local machine. You can do this by running the following command in your terminal:
```shell
npm install -g vercel
```

- Next, create a new directory for your project and navigate into it:

```shell
mkdir my-vercel-function && cd my-vercel-function
```

- In your project directory, create a new file that will contain your serverless function. You can do this by running the following command:

```shell
touch api/hello.js
```

- Open the hello.js file in your favorite text editor and add the following code:

```javascript
module.exports = (req, res) => {
  res.status(200).send("Hello, from Vercel!");
};
```

Now, deploy your serverless function by running the following command in your terminal:

```shell
vercel
```


Vercel will automatically detect the serverless function and deploy it to a serverless platform. Once the deployment is complete, Vercel will provide you with a unique URL to access your function.

## Testing the Function

After you've deployed your serverless function, you can test it by sending an HTTP request to the function's URL. You can do this using a tool like curl or Postman. Here's how to do it with curl:

- Open your terminal and run the following command:

```shell
curl https://my-vercel-function.vercel.app/api/hello
```

- Replace https://my-vercel-function.vercel.app/api/hello with the URL provided by Vercel after deployment.

- If everything is set up correctly, you should see the message "Hello, from Vercel!" in your terminal.

In conclusion, running serverless applications with Vercel is a straightforward process that involves setting up a Vercel account, deploying a serverless function, and testing the function. Vercel provides a simple and intuitive platform for deploying and managing serverless applications, making it a great choice for developers looking to leverage the benefits of serverless architecture.