variable "name_prefix" { type = string }
variable "vpc_cidr" { type = string, default = "10.40.0.0/16" }
variable "availability_zone_count" {
  type    = number
  default = 2
  validation {
    condition     = var.availability_zone_count >= 2 && var.availability_zone_count <= 3
    error_message = "Use 2 or 3 availability zones."
  }
}
variable "tags" { type = map(string), default = {} }
