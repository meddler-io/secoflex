Tools:
    Creation:
        Dockerfile
        Zip
        Tar
        Public Image
        Private Docker Image
            Credentials:
                Username / Password
                Auth




    Data formats: (needs to be flat)
        input:
            multi: boolean
            schema:
                -   id:
                    alias: Identifier
                    type: string (default) | enum | number (decimal / float) | url | file (minio_id)
                    tags: //array
                    visible: //array
                    meta: //object


        ouput:
            multi: boolean
            indexed: boolean
