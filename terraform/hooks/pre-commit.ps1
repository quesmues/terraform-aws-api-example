    $base_path = pwd
    $processed_paths = @()

    $diff = git diff --name-only
    $diff | % {
        $changed_path = split-path $_
    
        if($changed_path -notin $processed_paths) {
            cd $base_path/$changed_path && terraform fmt -recursive && `
            terraform init -backend=false && terraform validate

            $processed_paths += $changed_path
        }
    }