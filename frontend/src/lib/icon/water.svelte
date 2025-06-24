<script lang="ts">
    import type { iconProps } from ".";

    let {
        color,
        size = 20
    }: iconProps = $props()
</script>
<svg width={size} height={size} viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M11.7 10.8C11.2981 12.0573 10.2882 13.0627 8.99998 13.5001M9.00002 16.2001C6.02248 16.2001 3.59998 13.9185 3.59998 11.1141C3.59998 7.20005 9.00006 1.80005 9.00006 1.80005C9.00006 1.80005 14.4 7.20005 14.4 11.1141C14.4 13.9185 11.9776 16.2001 9.00002 16.2001Z" stroke={color} stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>