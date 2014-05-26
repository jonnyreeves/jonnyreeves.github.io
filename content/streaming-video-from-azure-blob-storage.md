Title: Streaming Video from Azure Blob Storage
Date: 2012-07-20 16:15
Category: Azure

By default Azure Blob Storage and Video do not mix well; the first hurdle that developers must get over is that the Content Type for the video must be set correctly (for .mp4 videos that’s usually `video/mp4`).

The next problem that you’ll face is that the video will not seek correctly; trying to jump forward or backwards in the video won’t work.

This is resolved by changing the `DefaultServiceVersion` to 2011-08-18 which can be achieved via the Azure’s REST API, or the Managed C# Library as laid out at the end of [this MSDN blog post](http://blogs.msdn.com/b/windowsazurestorage/archive/2011/09/15/windows-azure-blobs-improved-http-headers-for-resume-on-download-and-a-change-in-if-match-conditions.aspx).

```c#
var account = CloudStorageAccount.Parse(ConnectionString);
var blobClient = account.CreateCloudBlobClient();
blobClient.SetServiceSettings(new ServiceSettings()
    {
        DefaultServiceVersion = "2011-08-18"
    });
```