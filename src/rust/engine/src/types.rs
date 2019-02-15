use crate::core::{Function, TypeConstraint, TypeId};

pub struct Types {
  pub construct_directory_digest: Function,
  pub construct_snapshot: Function,
  pub construct_file_content: Function,
  pub construct_files_content: Function,
  pub construct_process_result: Function,
  pub address: TypeConstraint,
  pub path_globs: TypeConstraint,
  pub directory_digest: TypeConstraint,
  pub snapshot: TypeConstraint,
  pub merged_directories: TypeConstraint,
  pub files_content: TypeConstraint,
  pub dir: TypeConstraint,
  pub file: TypeConstraint,
  pub link: TypeConstraint,
  pub process_request: TypeConstraint,
  pub process_result: TypeConstraint,
  pub generator: TypeConstraint,
  pub url_to_fetch: TypeConstraint,
  pub string: TypeId,
  pub bytes: TypeId,
}
