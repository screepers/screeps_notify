declare module "notify" {
    function Notify(message: string, limit?: number, groups?: string[]): void;
    export = Notify;
}
