module "ecs" {
  source             = "../../i-ai-core-infrastructure//modules/ecs"
  project_name       = var.project_name
  image_tag          = "57aec8f3294bbc7002214c1b7ca7235615c2d0f6"
  prefix             = "i-dot-ai"
  ecr_repository_uri = var.ecr_repository_uri
  cluster_name       = var.cluster_name
  health_check = {
    healthy_threshold   = 3
    unhealthy_threshold = 3
    accepted_response   = "200"
    path                = "/"
    timeout             = 6
  }

  state_bucket                 = var.state_bucket
  vpc_id                       = data.terraform_remote_state.vpc.outputs.vpc_id
  private_subnets              = data.terraform_remote_state.vpc.outputs.private_subnets
  container_port               = "80"
  load_balancer_security_group = data.terraform_remote_state.platform.outputs.load_balancer_security_group_id["default"]
  aws_lb_arn                   = data.terraform_remote_state.platform.outputs.load_balancer_arn["default"]
}
