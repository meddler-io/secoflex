# Run / Execute Build


import logging
from app.models.tool.builds import AuthType
from app.models.tool import build
from app.models.tool.build.common import BaseBuildModel, BuildType
from app.models.tool.build import bundle_git
from app.models.tool.build import bundle_url
from app.models.tool.build import bundle_upload
from app.models.tool.build import dockerfile
from app.models.tool.build import private_registry
from app.models.tool.build import public_registry


def parseBuild(build_from_db: BaseBuildModel):

    args = {}
    dockerfile_path = None
    destination = None
    env = {

    }
    
    env["base_path"] = "/kaniko/fs"
    env["input_dir"] = "/input"

    result = build_from_db


    if result.build.type == BuildType.REGISTRY_PUBLIC:
        build = public_registry.DockerPublicUrlInDB(**result.dict())

        raise Exception("Unspported Operation: Build via REGISTRY_PUBLIC")
        pass
    elif result.build.type == BuildType.REGISTRY_PRIVATE:
        build = private_registry.DockerPrivateUrlInDB(**result.dict())
        raise Exception("Unspported Operation: Build via REGISTRY_PRIVATE")

        pass
    elif result.build.type == BuildType.BUNDLE_GIT:
        
        build = bundle_git.GitUrlInDB(**result.dict())
        env["BUILDCONTEXT"] = build.build.config.repository_url
        if build.auth.mode == AuthType.NONE:
            pass
        elif build.auth.mode == AuthType.CREDENTIALS:
            env["GIT_USERNAME"] = build.auth.auth.username
            env["GIT_PASSWORD"] = build.auth.auth.password
            pass
        elif build.auth.mode == AuthType.AUTHTOKEN:
            env["GIT_TOKEN"] = build.auth.auth.auth_token
            pass
        else:
            raise Exception(
                f"Unspported Operation: Build via {build.auth.mode} using unknown 'authmode': {build.auth.mode}")

        pass

        
    elif result.build.type == BuildType.BUNDLE_UPLOAD:
        build = bundle_upload.BundleUploadInDB(**result.dict())
        # args["build_context"] =  build.build.config.get_object_path()
        # Assuming uploaded package is tar
        env["BUILDCONTEXT"] = f"tar://$input_dir/{build.build.config.bucket}/{build.build.config.identifier}/{build.build.config.version}:{build.build.config.filename}"
        


        # env["BUILDCONTEXT"] ="s3://192.168.29.5:9000/uploadedbundles/test_id/fe559aeea5454e34a74e83d58a78b83f%3Aimage.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=MEDDLER%2F20210218%2Fmeddler%2Fs3%2Faws4_request&X-Amz-Date=20210218T220027Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=90c664dad4e81b2c98de087b5bc34b11b81ec97f46604c95a2f2d18e9cacbfdf"

        if build.auth.mode == AuthType.NONE:
            pass
        else:
            raise Exception(
                f"Unspported Operation: Build via {build.auth.mode} using unknown 'authmode': {build.auth.mode}")

        pass
    elif result.build.type == BuildType.BUNDLE_URL:
        build = bundle_url.BundleUrlInDB(**result.dict())
        raise Exception("Unspported Operation: Build via BUNDLE_URL")
    else:
        pass

    
    
    return {
        "args": args,
        "env": env
    }
